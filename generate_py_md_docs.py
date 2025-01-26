import os
import openai
from multiprocessing import Pool # Multiprocessing. Utilizing mulitiple CPU cores for speed.


# Include your own API key.
openai.api_key = ""

with open('./Readme.md', 'r') as file:
    markdown_format = file.read()

def get_python_files(folder_path):
    # Lists all files in the directory and filters them to return only those that end with .py.
    return [f for f in os.listdir(folder_path) if f.endswith('.py')]

def read_file(file_path):
    # Opens a specified file in read mode and returns its content as a string.
    with open(file_path, 'r') as file:
        return file.read()

def generate_markdown_output(content):
    # Sends a request to the OpenAI API, asking it to document the provided Python code.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"You're a seasoned developer with advanced skills in Python. Generate a step-by-step explanation of the codes made available to you. Use this file: {markdown_format} for reference:\n\n{content}"}
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