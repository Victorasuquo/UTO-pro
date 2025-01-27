import os
import openai
from multiprocessing import Pool # Multiprocessing. Utilizing mulitiple CPU cores for speed.


# Include your own API key.
openai.api_key = ""


def get_python_files(folder_path):
    python_files = []     

    # Walk through the directory tree
    for root, dirs, files in os.walk(folder_path):
        # Exclude the `.venv` folder from the search
        if '.venv' in dirs:
            dirs.remove('.venv')  # This prevents os.walk from traversing into .venv
        
        for file in files:
            if file.endswith('.py'):
                # Construct the full path to the file
                full_path = os.path.join(root, file)
                python_files.append(full_path)
    
    return python_files

def read_file(file_path):
    # Opens a specified file in read mode and returns its content as a string.
    with open(file_path, 'r') as file:
        return file.read()

def generate_markdown_output(content):
    # Sends a request to the OpenAI API, asking it to document the provided Python code.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": 
                f'''
                    Create a detailed and well-structured Markdown documentation for the provided Python files. 
                    Each documentation should be tailored to each files. The documentation should include the following sections:
                    Introduction: Provide a brief overview of the application, with its actual name of the file, its purpose, and the technologies it integrates with.
                    Prerequisites: List the requirements needed to run the application, such as Python version, OpenAI API key, etc.
                    Installation: Provide step-by-step instructions on how to clone the repository (if available) and install the necessary dependencies using pip.
                    Configuration: Explain how to set up the environment variables in a .env file, including the OpenAI API key and anything provided.
                    Usage: Describe how to start the application and access it via a local server.
                    Code Explanation: Break down the key components of the code, including:
                    Imports and environment variable loading
                    Application initialization
                    Helper functions for querying the OpenAI GPT model, parsing stories, and extracting tasks
                    Contributing: Provide guidelines for contributing to the project, including steps for forking the repository, creating a new branch, committing changes, and submitting a pull request.
                    License: Mention the license under which the project is distributed (e.g., MIT License) and provide a link to the license file.

                    Ensure that the documentation is clear, concise, and well-organized, with appropriate headings, subheadings, code blocks, and example JSON responses. 
                    Use Markdown formatting for code snippets, lists, and tables where necessary.
                    \n\n{content}
                '''}
        ]
    )
    return response['choices'][0]['message']['content']

def save_markdown_file(folder_path, file_name, content):
    # Creates the path for the Markdown file and writes the generated documentation to it.
    markdown_file_path = os.path.join(folder_path, f"{file_name}.md")
    with open(markdown_file_path, 'w') as md_file:
        md_file.write(content)
    print(f"Markdown file saved as: {markdown_file_path}")

def process_file(file_path):
    # Processes a single Python file to generate its documentation.
    code_content = read_file(file_path)
    markdown_content = generate_markdown_output(code_content)
    file_name = os.path.basename(file_path).replace('.py', '')
    save_markdown_file(os.path.dirname(file_path), file_name, markdown_content)

def generate_documentation():
    # Generates documentation for all Python files in the current directory using multiprocessing.
    folder_path = os.getcwd()  # Use the current working directory
    python_files = get_python_files(folder_path)
    
    if not python_files:
        print(f"No Python files found in the folder: {folder_path}")
        return

    file_paths = [os.path.join(folder_path, f) for f in python_files]
    
    with Pool() as pool:
        # For concurrency. Handling multiple files simultaneously
        pool.map(process_file, file_paths)
    
    print("Documentation generated successfully for all Python files.")

if __name__ == "__main__":
    generate_documentation()