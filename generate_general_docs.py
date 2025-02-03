import os
import openai
import multiprocessing
from dotenv import load_dotenv

def find_markdown_files(directory):
    """Recursively search for .md files in the given directory."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
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
    """Use OpenAI to generate concise and accurate markdown documentation."""
    prompt = """
    You are an AI that generates high-quality markdown documentation. Below are the contents of multiple markdown files.
    Analyze them and generate a structured documentation file that concisely describes the purpose of each file, referencing them correctly.

    Markdown File Contents:
    """
    for file, content in file_contents.items():
        prompt += f"\n### File: {os.path.basename(file)}\n\n{content[:1000]}\n\n"  # Limit content to avoid token overload
    
    prompt += """
    Generate a final documentation in markdown format, clearly referencing the individual files.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful AI that writes documentation."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have set this environment variable
    
    directory = os.getcwd()
    markdown_files = find_markdown_files(directory)
    
    if not markdown_files:
        print("No .md files found.")
        return
    
    file_contents = read_markdown_files(markdown_files)
    documentation = generate_documentation(file_contents)
    
    with open(os.path.join(directory, "GENERAL DOCUMENTATION.md"), "w", encoding='utf-8') as doc_file:
        doc_file.write(documentation)
    
    print("Generated GENERAL DOCUMENTATION.md in the specified directory.")

if __name__ == "__main__":
    main()