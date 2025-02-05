# Python Markdown Documentation Generator

This document provides detailed and structured documentation for the Python script that generates documentation for markdown files using OpenAI's ChatCompletion API.

---

## Overview

This script automates the process of generating structured markdown documentation for markdown (`.md`) files located within a given directory. It accomplishes the following tasks:

- Recursively searches for markdown files while excluding folders like `.venv`.
- Reads the content of these files, handling potential Unicode decoding issues.
- Utilizes multiprocessing to read files in parallel for efficiency.
- Constructs a custom prompt and uses OpenAI's API to generate comprehensive documentation.
- Writes the generated documentation to a file named `3o_mini.md` in the current working directory.

---

## Installation & Dependencies

### Required Dependencies

- Python 3.x
- [openai](https://pypi.org/project/openai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

### Installation Steps

1. Install Python 3.x if not already installed.
2. Use `pip` to install the required packages:

   ```bash
   pip install openai python-dotenv
   ```

3. Ensure that you set your OpenAI API key in a `.env` file with the following content:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

---

## Usage

1. Place the script in your project directory where you have markdown files.
2. Execute the script from the command line:

   ```bash
   python script_name.py
   ```

3. The script will search for `.md` files, generate documentation by interacting with the OpenAI API, and create a file named `3o_mini.md` containing the generated documentation.

4. If no markdown files are found, the script prints an appropriate message: "No .md files found."

---

## Function/Class Documentation

### find_markdown_files(folder_path)

- **Purpose:** Recursively search for `.md` files in a given directory while excluding any directories that contain `.venv`.
- **Parameters:**
  - `folder_path` (str): The root directory path where the search should begin.
- **Returns:** 
  - `list`: A list of paths (str) pointing to all found markdown files.

---

### read_file(file)

- **Purpose:** Reads the content of a markdown file while handling potential encoding issues.
- **Parameters:**
  - `file` (str): The file path to read.
- **Returns:** 
  - `tuple`: A tuple where the first element is the file path (str) and the second element is the file content (str).
- **Error Handling:** Uses a try/except block to switch encoding methods if a `UnicodeDecodeError` is encountered.

---

### read_markdown_files(files)

- **Purpose:** Reads multiple markdown files concurrently using the multiprocessing module.
- **Parameters:**
  - `files` (list): A list of file paths (str) to read.
- **Returns:**
  - `dict`: A dictionary with file paths as keys and their respective contents as values.

---

### generate_documentation(file_contents)

- **Purpose:** Constructs a prompt containing file contents and sends it to the OpenAI API to generate a well-structured markdown documentation.
- **Parameters:**
  - `file_contents` (dict): A dictionary with markdown file paths and their corresponding contents.
- **Returns:**
  - `str`: Generated markdown documentation as returned by the OpenAI API.
- **Details:**
  - Constructs clickable relative links for individual files.
  - Includes initial portions of file content (first 1000 characters) for context.
  - Uses the `openai.ChatCompletion.create` method to get the final documentation.

---

### main()

- **Purpose:** Orchestrates the overall process: loading environment variables, searching for files, reading file contents, generating documentation, and writing the final documentation file.
- **Process Overview:**
  1. Loads `.env` environment variables.
  2. Sets the OpenAI API key from the environment.
  3. Searches the current working directory for markdown files using `find_markdown_files()`.
  4. If markdown files are found, reads their content in parallel using `read_markdown_files()`.
  5. Generates markdown documentation via `generate_documentation()`.
  6. Writes the generated documentation to `3o_mini.md`.
- **Output:** Prints the path of the generated documentation file or a message if no markdown files are found.

---

## Code Walkthrough

1. **Imports & Setup:**
   - Imports necessary modules: `os`, `openai`, `multiprocessing`, and `load_dotenv` from `dotenv`.
   - Loads environment variables to retrieve the OpenAI API key.

2. **Searching for Markdown Files:**
   - `find_markdown_files(folder_path)` recursively walks the directory tree (using `os.walk`).
   - Excludes any directory containing `.venv` to avoid processing virtual environment files.
   - Collects and returns a list of `.md` file paths.

3. **Reading File Contents with Error Handling:**
   - `read_file(file)` attempts to read a file with `utf-8` encoding.
   - Falls back to `latin-1` encoding with error replacement if a `UnicodeDecodeError` occurs.
   - `read_markdown_files(files)` utilizes `multiprocessing.Pool` to process files concurrently, enhancing performance.

4. **Generating Documentation via OpenAI:**
   - `generate_documentation(file_contents)` creates a prompt that includes:
     - An introductory instruction for the AI.
     - A detailed listing of each markdown file (including formatted links and a snippet of contents).
   - Sends the prompt to the OpenAI ChatCompletion API.
   - Receives and returns the AI-generated documentation.

5. **Writing Documentation to File:**
   - The `main()` function ties all components together:
     - Loads environment variables.
     - Searches for `.md` files.
     - If found, processes and generates documentation.
     - Writes the result to `3o_mini.md` in the current directory.
     - Outputs a confirmation message indicating the location of the generated file.

---

## Example Output

If the script successfully generates documentation, you might see an output similar to:

```
Generated 3o_mini.md in /path/to/your/directory/3o_mini.md.
```

The generated `3o_mini.md` file will contain structured markdown that includes clickable file links and snippets of markdown file contents, for example:

```markdown
# Project Documentation

## [example.md](./example.md)

```
# Example Markdown Content...
...
```

...
```

---

## Error Handling

- **File Reading:** 
  - The `read_file()` function gracefully handles `UnicodeDecodeError` by trying an alternate encoding (`latin-1`) with error replacement.
  
- **Missing Files:**
  - If no markdown files are found in the directory, the `main()` function prints "No .md files found." and exits without attempting further processing.

- **API Interaction:**
  - Although not explicitly surrounded by try/except blocks for the API call, any errors from the OpenAI API will propagate as exceptions. Consider wrapping `openai.ChatCompletion.create()` in a try/except block for production environments to manage API errors.

---

This comprehensive documentation outlines how the Python script works, its dependencies, usage, and the functionality of each part of the code, facilitating easy understanding and potential future modifications.