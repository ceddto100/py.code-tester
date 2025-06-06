# Python Code Testing Environment

A containerized Python testing environment with data science and development libraries, designed for both beginners and advanced users.

## Features

- **Fully-equipped Python environment** with pre-installed libraries (NumPy, Pandas, Matplotlib, TensorFlow, etc.)
- **Modern web-based UI** with code editor and output display
- **Code execution with safety constraints** (sandboxed environment, timeout functionality)
- **Built-in visualization support** for matplotlib/seaborn plots
- **File management** for saving and loading Python scripts
- **Code tools** including formatter (Black) and linter (Pylint)
- **Light and dark themes** for comfortable coding experience

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- Git (optional, for cloning the repository)

### Installation

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/python-testing-env.git
   cd python-testing-env
   ```

2. Build and start the environment using Docker Compose:
   ```
   docker-compose up -d
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Using the Environment

1. **Code Editor**: Write or paste your Python code in the editor pane.
2. **Run Code**: Click the "Run Code" button (or press Ctrl+Enter) to execute.
3. **View Results**: Output will be displayed in the output pane with tabs for regular output, errors, and visualizations.
4. **File Operations**:
   - Create a new file with the File → New menu option
   - Open existing files with File → Open
   - Save your work with File → Save

## Safety Features

- **Sandboxed Execution**: Code runs in a containerized environment
- **Resource Limits**: Memory usage caps and execution timeouts
- **Restricted Access**: Limited file system and network access

## Libraries and Tools

The environment comes with the following Python libraries pre-installed:

- **Data Analysis**: NumPy, Pandas, SciPy
- **Visualization**: Matplotlib, Seaborn
- **Testing**: Pytest
- **Web Development**: Flask, Requests
- **Web Scraping**: BeautifulSoup4
- **Natural Language Processing**: NLTK
- **Machine Learning**: TensorFlow (CPU), PyTorch (CPU)
- **Development Tools**: Black (formatter), Pylint (linter)

## Examples

Check the `user_code/examples` directory for sample scripts demonstrating various features and libraries.

## Troubleshooting

- **Container won't start**: Make sure ports 5000 is available on your system
- **Memory issues**: Adjust memory limits in docker-compose.yml
- **Slow performance**: Consider reducing the number of installed libraries in requirements.txt

## Customization

- **Adding libraries**: Modify the requirements.txt file and rebuild the container
- **Changing memory/time limits**: Edit the environment variables in docker-compose.yml
- **UI customization**: Modify the templates and static files

## License

This project is licensed under the MIT License - see the LICENSE file for details. #   p y . c o d e - t e s t e r  
 