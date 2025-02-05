import os
import openai
from multiprocessing import Pool # Multiprocessing. Utilizing mulitiple CPU cores for speed.


# Include your own API key.
openai.api_key = "sk-svcacct--MpjIFRme5uSgt2Rmf9127aywUm7We0RzyPgdE2lOkgJQLh72OGbNdSbjo6wkyVQMqq0KT3BlbkFJ66NtEZtJj4kxP5OBeBIg78RtIxYc_deo9jNOGyJoT_BIkjmizwSmD1S2QsSAuKEqkRmAA"


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
        model="o3-mini",
        messages=[
            {"role": "user", "content": 
                f'''
                    "You are an AI assistant that generates detailed and structured documentation for Python code in markdown format. 
                    Your goal is to analyze the given Python script and produce well-formatted documentation with the following details:

                    1. *Title*: A brief and descriptive title for the script.
                    2. *Overview*: A high-level summary of what the script does.
                    3. *Installation & Dependencies*: List any required dependencies or installation steps (if applicable).
                    4. *Usage*: Explain how to run the script with examples.
                    5. *Function/Class Documentation*: 
                    - For each function and class, provide:
                        - A brief summary of its purpose.
                        - Input parameters (names, types, and descriptions).
                        - Return values (types and descriptions).
                    6. *Code Walkthrough*: Explain the key sections of the script step by step.
                    7. *Example Output*: If applicable, provide sample output or expected behavior.
                    8. *Error Handling*: Highlight any error handling mechanisms in the code.

                    Generate the documentation in *markdown format* with appropriate headings (#, ##, ###), lists (-), and code blocks (```). 
                    Maintain clarity and conciseness while ensuring completeness.

                    Here is the Python script to document:\n\n{content}
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