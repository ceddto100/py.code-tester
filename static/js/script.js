document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror
    const editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        autoCloseBrackets: true,
        styleActiveLine: true,
        tabSize: 4,
        extraKeys: {
            'Tab': function(cm) {
                // Replace Tab with 4 spaces
                const spaces = ' '.repeat(cm.getOption('indentUnit'));
                cm.replaceSelection(spaces);
            },
            'Ctrl-Space': 'autocomplete'
        }
    });

    // Set initial sample code
    const sampleCode = `# Welcome to the Python Testing Environment!
# This is a sample code to get you started.

import numpy as np
import matplotlib.pyplot as plt

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a simple plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sine Wave')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.grid(True)

# Display the plot
plt.show()

# Print some information
print("Hello, World!")
print("NumPy version:", np.__version__)
print("Array example:", np.random.rand(5))
`;
    editor.setValue(sampleCode);

    // Track current file
    let currentFile = null;

    // UI elements
    const runCodeBtn = document.getElementById('runCode');
    const clearOutputBtn = document.getElementById('clearOutput');
    const outputText = document.getElementById('outputText');
    const errorText = document.getElementById('errorText');
    const visualOutput = document.getElementById('visualOutput');
    const fileList = document.getElementById('fileList');
    const openFileList = document.getElementById('openFileList');
    const newFileBtn = document.getElementById('newFile');
    const openFileBtn = document.getElementById('openFile');
    const saveFileBtn = document.getElementById('saveFile');
    const saveFileModal = new bootstrap.Modal(document.getElementById('saveFileModal'));
    const openFileModal = new bootstrap.Modal(document.getElementById('openFileModal'));
    const formatCodeBtn = document.getElementById('formatCode');
    const lintCodeBtn = document.getElementById('lintCode');
    const themeDarkBtn = document.getElementById('themeDark');
    const themeLightBtn = document.getElementById('themeLight');
    const currentFileName = document.getElementById('currentFileName');
    const refreshFilesBtn = document.getElementById('refreshFiles');
    const quickNewBtn = document.getElementById('quickNew');
    const copyOutputBtn = document.getElementById('copyOutput');
    const fileSearchInput = document.getElementById('fileSearch');
    const examplesList = document.getElementById('examplesList');
    
    // Event listeners
    runCodeBtn.addEventListener('click', runCode);
    clearOutputBtn.addEventListener('click', clearOutput);
    newFileBtn.addEventListener('click', newFile);
    openFileBtn.addEventListener('click', openFile);
    saveFileBtn.addEventListener('click', () => saveFileModal.show());
    document.getElementById('saveFileBtn').addEventListener('click', saveFile);
    formatCodeBtn.addEventListener('click', formatCode);
    lintCodeBtn.addEventListener('click', lintCode);
    themeDarkBtn.addEventListener('click', () => setTheme('dark'));
    themeLightBtn.addEventListener('click', () => setTheme('light'));
    refreshFilesBtn && refreshFilesBtn.addEventListener('click', updateFileList);
    quickNewBtn && quickNewBtn.addEventListener('click', newFile);
    copyOutputBtn && copyOutputBtn.addEventListener('click', copyOutput);
    fileSearchInput && fileSearchInput.addEventListener('input', filterFiles);

    // Run code function
    function runCode() {
        // Clear previous output
        clearOutput();
        
        // Get the code from the editor
        const code = editor.getValue();
        
        // Show loading indicator
        runCodeBtn.innerHTML = '<span class="spinner"></span> Running...';
        runCodeBtn.disabled = true;
        
        // Send the code to the server for execution
        fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            // Display the output
            outputText.textContent = data.stdout || 'No output';
            errorText.textContent = data.stderr || 'No errors';
            
            // Display visualizations
            if (data.figures && data.figures.length > 0) {
                data.figures.forEach(imgData => {
                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,' + imgData;
                    visualOutput.appendChild(img);
                });
                
                // Activate the Visualizations tab if there are figures
                document.getElementById('visual-tab').click();
            } else if (data.stderr && data.stderr.trim() !== '') {
                // Activate the Errors tab if there are errors
                document.getElementById('error-tab').click();
            } else {
                // Activate the Output tab by default
                document.getElementById('output-tab').click();
            }
            
            // Hide loading indicator
            runCodeBtn.innerHTML = '<i class="fas fa-play me-1"></i> Run Code';
            runCodeBtn.disabled = false;
            
            // Show toast notification
            showToast('Code executed successfully');
        })
        .catch(error => {
            console.error('Error:', error);
            errorText.textContent = 'Error: ' + error.message;
            document.getElementById('error-tab').click();
            
            // Hide loading indicator
            runCodeBtn.innerHTML = '<i class="fas fa-play me-1"></i> Run Code';
            runCodeBtn.disabled = false;
            
            // Show error toast
            showToast('Error executing code', 'error');
        });
    }

    // Clear output function
    function clearOutput() {
        outputText.textContent = '';
        errorText.textContent = '';
        visualOutput.innerHTML = '';
    }

    // New file function
    function newFile() {
        if (confirm('Create a new file? Any unsaved changes will be lost.')) {
            editor.setValue('# New Python file\n\n');
            clearOutput();
            currentFile = null;
            updateFileName('Code Editor');
        }
    }

    // Open file function
    function openFile() {
        // Fetch available files
        fetch('/api/load')
        .then(response => response.json())
        .then(data => {
            // Clear previous file list
            openFileList.innerHTML = '';
            
            // Add each file to the list
            if (data.files.length > 0) {
                data.files.forEach(file => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    
                    // Add icon based on file type
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-file-code me-2';
                    item.appendChild(icon);
                    
                    // Add file name
                    const text = document.createTextNode(file);
                    item.appendChild(text);
                    
                    item.addEventListener('click', function() {
                        loadFile(file);
                        openFileModal.hide();
                    });
                    openFileList.appendChild(item);
                });
                
                // Initialize file search
                if (fileSearchInput) {
                    fileSearchInput.value = '';
                }
            } else {
                const item = document.createElement('div');
                item.className = 'list-group-item text-center py-3';
                item.innerHTML = '<i class="fas fa-info-circle me-2"></i>No files available';
                openFileList.appendChild(item);
            }
            
            // Show the modal
            openFileModal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading files: ' + error.message, 'error');
        });
    }

    // Load file function
    function loadFile(filename) {
        fetch('/api/load/' + filename)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                editor.setValue(data.code);
                clearOutput();
                currentFile = filename;
                updateFileName(filename);
                showToast(`File "${filename}" loaded`);
            } else {
                showToast('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading file: ' + error.message, 'error');
        });
    }

    // Save file function
    function saveFile() {
        const filename = document.getElementById('saveFileName').value;
        if (!filename) {
            showToast('Please enter a file name', 'warning');
            return;
        }
        
        const code = editor.getValue();
        
        fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                filename: filename,
                code: code 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                saveFileModal.hide();
                showToast(`File "${filename}" saved successfully!`);
                // Update current file
                currentFile = filename;
                updateFileName(filename);
                // Refresh file list
                updateFileList();
            } else {
                showToast('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error saving file: ' + error.message, 'error');
        });
    }

    // Format code function
    function formatCode() {
        const code = editor.getValue();
        
        fetch('/api/format', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorText.textContent = 'Formatting error: ' + data.error;
                document.getElementById('error-tab').click();
                showToast('Error formatting code', 'error');
            } else {
                editor.setValue(data.code);
                showToast('Code formatted successfully');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorText.textContent = 'Error: ' + error.message;
            document.getElementById('error-tab').click();
            showToast('Error: ' + error.message, 'error');
        });
    }

    // Lint code function
    function lintCode() {
        const code = editor.getValue();
        
        fetch('/api/lint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorText.textContent = 'Linting error: ' + data.error;
                showToast('Linting error', 'error');
            } else if (data.issues && data.issues.length > 0) {
                let lintOutput = 'Linting issues found:\n\n';
                data.issues.forEach(issue => {
                    lintOutput += `Line ${issue.line}, Column ${issue.column}: ${issue.message} (${issue.symbol})\n`;
                    // Highlight the line in the editor
                    editor.addLineClass(issue.line - 1, 'background', 'cm-error-line');
                });
                errorText.textContent = lintOutput;
                showToast(`Found ${data.issues.length} linting issues`, 'warning');
            } else {
                errorText.textContent = 'No linting issues found';
                showToast('No linting issues found', 'success');
            }
            document.getElementById('error-tab').click();
        })
        .catch(error => {
            console.error('Error:', error);
            errorText.textContent = 'Error: ' + error.message;
            document.getElementById('error-tab').click();
            showToast('Error: ' + error.message, 'error');
        });
    }

    // Set theme function
    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            editor.setOption('theme', 'monokai');
        } else {
            document.body.classList.remove('dark-mode');
            editor.setOption('theme', 'default');
        }
        
        // Store preference in localStorage
        localStorage.setItem('theme', theme);
    }

    // Update file list function
    function updateFileList() {
        fetch('/api/load')
        .then(response => response.json())
        .then(data => {
            // Clear previous file list
            fileList.innerHTML = '';
            
            // Add each file to the list
            if (data.files.length > 0) {
                data.files.forEach(file => {
                    const item = document.createElement('li');
                    
                    // Add icon
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-file-code me-2';
                    item.appendChild(icon);
                    
                    // Add file name
                    const text = document.createTextNode(file);
                    item.appendChild(text);
                    
                    // Highlight current file
                    if (currentFile === file) {
                        item.classList.add('active', 'fw-bold');
                    }
                    
                    item.addEventListener('click', function() {
                        loadFile(file);
                    });
                    fileList.appendChild(item);
                });
                
                // Also update examples dropdown
                updateExamplesList(data.files);
            } else {
                const item = document.createElement('li');
                item.innerHTML = '<i class="fas fa-info-circle me-2"></i>No files available';
                fileList.appendChild(item);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    // Update examples list in the dropdown
    function updateExamplesList(files) {
        // Clear the list
        examplesList.innerHTML = '';
        
        // Filter for examples
        const examples = files.filter(file => file.startsWith('examples/') || file.includes('example'));
        
        if (examples.length > 0) {
            examples.forEach(file => {
                const item = document.createElement('li');
                const link = document.createElement('a');
                link.className = 'dropdown-item';
                link.href = '#';
                
                const icon = document.createElement('i');
                icon.className = 'fas fa-file-code me-2';
                link.appendChild(icon);
                
                // Clean up the example name for display
                let displayName = file.replace('examples/', '').replace('.py', '');
                // Convert snake_case to Title Case
                displayName = displayName.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                ).join(' ');
                
                const text = document.createTextNode(displayName);
                link.appendChild(text);
                
                link.addEventListener('click', function() {
                    loadFile(file);
                });
                
                item.appendChild(link);
                examplesList.appendChild(item);
            });
        } else {
            const item = document.createElement('li');
            const link = document.createElement('a');
            link.className = 'dropdown-item disabled';
            link.href = '#';
            link.textContent = 'No examples available';
            item.appendChild(link);
            examplesList.appendChild(item);
        }
    }
    
    // Update file name in the editor header
    function updateFileName(name) {
        if (currentFileName) {
            currentFileName.textContent = name;
        }
    }
    
    // Filter files in the open file dialog
    function filterFiles() {
        const searchTerm = fileSearchInput.value.toLowerCase();
        const items = openFileList.querySelectorAll('a.list-group-item');
        
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    // Copy output to clipboard
    function copyOutput() {
        const activeTab = document.querySelector('#outputTabs .nav-link.active');
        let textToCopy = '';
        
        if (activeTab.id === 'output-tab') {
            textToCopy = outputText.textContent;
        } else if (activeTab.id === 'error-tab') {
            textToCopy = errorText.textContent;
        } else {
            // Visual tab - just show a message
            showToast('Cannot copy visualizations directly', 'info');
            return;
        }
        
        if (textToCopy.trim() === '') {
            showToast('Nothing to copy', 'info');
            return;
        }
        
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                showToast('Copied to clipboard');
            })
            .catch(err => {
                console.error('Error copying to clipboard:', err);
                showToast('Failed to copy to clipboard', 'error');
            });
    }
    
    // Toast notification function
    function showToast(message, type = 'success') {
        // Remove any existing toasts
        const existingToasts = document.querySelectorAll('.toast-notification');
        existingToasts.forEach(toast => toast.remove());
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        
        // Add icon based on type
        let icon = 'check-circle';
        if (type === 'error') icon = 'exclamation-circle';
        if (type === 'warning') icon = 'exclamation-triangle';
        if (type === 'info') icon = 'info-circle';
        
        toast.innerHTML = `<i class="fas fa-${icon} me-2"></i>${message}`;
        
        // Add to the document
        document.body.appendChild(toast);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('hide');
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    // Initialize file list
    updateFileList();
    
    // Load theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to run code
        if (e.ctrlKey && e.key === 'Enter') {
            runCode();
            e.preventDefault();
        }
        
        // Ctrl+S to save
        if (e.ctrlKey && e.key === 's') {
            if (currentFile) {
                // Save current file directly
                const code = editor.getValue();
                fetch('/api/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        filename: currentFile,
                        code: code 
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(`File "${currentFile}" saved`);
                    } else {
                        showToast('Error: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showToast('Error saving file', 'error');
                });
            } else {
                // Show save dialog
                saveFileModal.show();
            }
            e.preventDefault();
        }
    });
    
    // Add CSS for toast notifications
    const style = document.createElement('style');
    style.textContent = `
        .toast-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 20px;
            background-color: #4caf50;
            color: white;
            border-radius: 4px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            z-index: 9999;
            font-size: 14px;
            animation: slideIn 0.3s ease-out;
        }
        
        .toast-error {
            background-color: #f44336;
        }
        
        .toast-warning {
            background-color: #ff9800;
        }
        
        .toast-info {
            background-color: #2196f3;
        }
        
        .toast-notification.hide {
            animation: slideOut 0.5s ease-out forwards;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .file-list li.active {
            background-color: rgba(98, 0, 238, 0.1);
        }
        
        body.dark-mode .file-list li.active {
            background-color: rgba(3, 218, 198, 0.1);
        }
        
        kbd {
            background-color: #eee;
            border-radius: 3px;
            border: 1px solid #b4b4b4;
            box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
            color: #333;
            display: inline-block;
            font-size: 0.85em;
            font-weight: 600;
            line-height: 1;
            padding: 2px 5px;
            white-space: nowrap;
        }
        
        body.dark-mode kbd {
            background-color: #333;
            border-color: #666;
            color: #eee;
        }
    `;
    document.head.appendChild(style);
}); 