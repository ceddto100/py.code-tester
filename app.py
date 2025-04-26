import os
import sys
import io
import json
import traceback
import signal
import threading
import tempfile
import psutil
import time
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import contextlib
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import logging
from dotenv import load_dotenv
import platform

# Try to import resource module (Unix-only)
is_windows = platform.system() == 'Windows'
if not is_windows:
    import resource

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Environment configuration
MAX_EXECUTION_TIME = int(os.environ.get('MAX_EXECUTION_TIME', 30))  # seconds
MAX_MEMORY_MB = int(os.environ.get('MAX_MEMORY_MB', 500))  # MB

# Ensure directories exist
os.makedirs('user_code', exist_ok=True)
os.makedirs('output', exist_ok=True)

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

class MemoryLimitError(Exception):
    pass

def limit_memory_usage():
    """Limit memory usage for the current process."""
    if not is_windows:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_MB * 1024 * 1024, hard))
    # On Windows, we'll use psutil for monitoring instead

class OutputCapture:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.figures = []
        
    @contextlib.contextmanager
    def capture(self):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.stdout, self.stderr
        
        # Capture matplotlib figures
        old_show = plt.show
        def custom_show(*args, **kwargs):
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_data = base64.b64encode(buf.read()).decode('utf-8')
            self.figures.append(img_data)
            plt.close(fig)
        
        plt.show = custom_show
        
        try:
            yield self
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
            plt.show = old_show

def run_code(code, timeout=MAX_EXECUTION_TIME):
    """Run Python code with timeout and resource limits."""
    output = OutputCapture()
    
    def execute():
        try:
            with output.capture():
                # Create a local namespace for execution
                local_vars = {}
                
                # Execute the code
                exec(code, local_vars)
        except Exception as e:
            traceback.print_exc(file=output.stderr)
    
    # Create a thread for execution
    thread = threading.Thread(target=execute)
    
    # Set timeout handler if not on Windows
    if not is_windows:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
    
    thread.start()
    
    try:
        # Wait for thread to complete
        thread.join(timeout)
        
        # Check if thread is still alive (timeout occurred)
        if thread.is_alive():
            raise TimeoutError("Code execution timed out")
        
        # Cancel the alarm if not on Windows
        if not is_windows:
            signal.alarm(0)
    except TimeoutError:
        output.stderr.write("ERROR: Code execution timed out after {} seconds\n".format(timeout))
    except MemoryLimitError:
        output.stderr.write("ERROR: Memory limit exceeded ({}MB)\n".format(MAX_MEMORY_MB))
    except Exception as e:
        output.stderr.write(f"ERROR: {str(e)}\n")
    
    # Return captured output
    return {
        'stdout': output.stdout.getvalue(),
        'stderr': output.stderr.getvalue(),
        'figures': output.figures
    }

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
def execute_code():
    """API endpoint to execute Python code."""
    data = request.json
    code = data.get('code', '')
    
    # Create a file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='user_code') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Monitor memory usage in a separate thread
        def monitor_memory():
            process = psutil.Process(os.getpid())
            while True:
                mem_usage = process.memory_info().rss / (1024 * 1024)  # MB
                if mem_usage > MAX_MEMORY_MB:
                    # On Windows, we can't send SIGTERM, so we'll just log and break
                    if is_windows:
                        logger.error("Memory limit exceeded")
                        break
                    else:
                        os.kill(os.getpid(), signal.SIGTERM)
                        break
                time.sleep(0.1)
        
        memory_monitor = threading.Thread(target=monitor_memory)
        memory_monitor.daemon = True
        memory_monitor.start()
        
        # Run the code
        result = run_code(code)
        
        # Format error messages with line numbers
        if result['stderr']:
            error_lines = result['stderr'].split('\n')
            formatted_errors = []
            for line in error_lines:
                if 'line' in line and temp_file in line:
                    # Extract line number from error message
                    try:
                        line_num = int(line.split('line')[1].split(',')[0].strip())
                        # Adjust line number for actual code
                        formatted_errors.append(line.replace(temp_file, 'your code'))
                    except:
                        formatted_errors.append(line)
                else:
                    formatted_errors.append(line)
            result['stderr'] = '\n'.join(formatted_errors)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        return jsonify({
            'stdout': '',
            'stderr': f"Server error: {str(e)}",
            'figures': []
        }), 500
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.route('/api/save', methods=['POST'])
def save_code():
    """Save code to a file."""
    data = request.json
    code = data.get('code', '')
    filename = data.get('filename', '')
    
    if not filename:
        return jsonify({'success': False, 'error': 'Filename is required'}), 400
    
    # Ensure the filename is safe
    filename = os.path.basename(filename)
    if not filename.endswith('.py'):
        filename += '.py'
    
    filepath = os.path.join('user_code', filename)
    try:
        with open(filepath, 'w') as f:
            f.write(code)
        return jsonify({'success': True, 'path': filepath})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load', methods=['GET'])
def list_files():
    """List available Python files."""
    files = [f for f in os.listdir('user_code') if f.endswith('.py')]
    return jsonify({'files': files})

@app.route('/api/load/<filename>', methods=['GET'])
def load_file(filename):
    """Load code from a file."""
    filepath = os.path.join('user_code', os.path.basename(filename))
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/lint', methods=['POST'])
def lint_code():
    """Lint Python code."""
    data = request.json
    code = data.get('code', '')
    
    # Create a temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Run pylint on the file
        from pylint import lint
        from pylint.reporters.text import TextReporter
        
        class CustomReporter(TextReporter):
            def __init__(self):
                self.messages = []
                super().__init__()
            
            def handle_message(self, msg):
                self.messages.append({
                    'line': msg.line,
                    'column': msg.column,
                    'type': msg.category,
                    'message': msg.msg,
                    'symbol': msg.symbol
                })
        
        reporter = CustomReporter()
        args = ['--errors-only', temp_file]
        lint.Run(args, reporter=reporter, exit=False)
        
        return jsonify({
            'issues': reporter.messages
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.route('/api/format', methods=['POST'])
def format_code():
    """Format Python code using Black."""
    data = request.json
    code = data.get('code', '')
    
    try:
        import black
        
        formatted_code = black.format_str(code, mode=black.Mode())
        return jsonify({
            'code': formatted_code
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': code  # Return original code on error
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 