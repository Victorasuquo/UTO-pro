import os
import openai
import multiprocessing
from dotenv import load_dotenv

def find_markdown_files(folder_path):
    """Recursively search for .md files in the given directory, excluding .venv."""
    markdown_files = []
    for root, dirs, files in os.walk(folder_path):
        if '.venv' in root.split(os.sep):  # Skip any folder inside .venv
            continue
        
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    return markdown_files

def read_file(file):
    """Read the content of a markdown file, handling encoding issues."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return file, f.read()
    except UnicodeDecodeError:
        with open(file, 'r', encoding='latin-1', errors='replace') as f:
            return file, f.read()

def read_markdown_files(files):
    """Read markdown files in parallel using multiprocessing."""
    with multiprocessing.Pool() as pool:
        file_contents = dict(pool.map(read_file, files))
    return file_contents

def generate_documentation(file_contents):
    """Use OpenAI to generate structured markdown documentation with accurate references."""
    prompt = """
    You are an AI that generates high-quality markdown documentation. Below are the contents of multiple markdown files.
    Analyze them and generate a structured documentation file that concisely describes the purpose of each file, referencing them with full paths correctly.

    Markdown File Contents:
    """
    
    documentation = "# Project Documentation\n\n"
    
    for file, content in file_contents.items():
        file_name = os.path.basename(file)  # Get only the filename
        relative_path = os.path.relpath(file, os.getcwd()).replace("\\", "/")  # Normalize path for Markdown
        file_link = f"[{file_name}]({relative_path})"  # Create Markdown-compatible relative links
        documentation += f"## {file_link}\n\n```\n{content[:1000]}\n```\n\n"  # Display the first 1000 characters
    
    prompt += documentation
    prompt += """
    Generate a final documentation in markdown format, clearly referencing the individual files with their relative paths as clickable links.
    """
    
    response = openai.ChatCompletion.create(
        model="o3-mini",
        messages=[{"role": "system", "content": "You are a helpful AI that writes documentation."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have set this environment variable
    
    file_path = os.getcwd()
    markdown_files = find_markdown_files(file_path)
    
    if not markdown_files:
        print("No .md files found.")
        return
    
    file_contents = read_markdown_files(markdown_files)
    documentation = generate_documentation(file_contents)
    
    doc_path = os.path.join(file_path, "3o_mini.md")
    with open(doc_path, "w", encoding='utf-8') as doc_file:
        doc_file.write(documentation)
    
    print(f"Generated 3o_mini.md in {doc_path}.")

if __name__ == "__main__":
    main()
