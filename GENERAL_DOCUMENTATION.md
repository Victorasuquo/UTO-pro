# Project Documentation

This documentation serves as a comprehensive guide to the various Python scripts and their functionalities within this project. Each script is responsible for specific tasks related to project management, GitHub interaction, and document querying through the integration of various libraries and APIs.

## Contents

- [Flask Web Application for Project Management](#flask-web-application-for-project-management)
- [Python Documentation Generator](#python-documentation-generator)
- [Hello World Script](#hello-world-script)
- [Document Querying with PDF Input](#document-querying-with-pdf-input)
- [Document QA System](#document-qa-system)
- [Intelligent Document Query System (UTOM)](#intelligent-document-query-system-utom)
- [GitHub API Fetcher](#github-api-fetcher)
- [GitHub Repository Analyzer](#github-repository-analyzer)
- [GitHub Issues and Repositories Inquiry Tool](#github-issues-and-repositories-inquiry-tool)
- [Note Tool Script](#note-tool-script)
- [Chat with GitHub README Files](#chat-with-github-readme-files)

---

## Flask Web Application for Project Management

Documentation for the Flask web application that manages project workflows by integrating with OpenAI's GPT model and MongoDB.

- **File**: [endpoint_.md](endpoint_.md)
- **Overview**: Implements project management features including project initialization, user input handling for stories and plans, and state management with MongoDB.
- **Installation & Dependencies**: Requires `Flask`, `pymongo`, `python-dotenv`, and `openai`.
- **Usage Instructions**: Execute the script with Python after configuring the necessary environment variables.

---

## Python Documentation Generator

Automates the generation of markdown documentation for Python files.

- **File**: [generate_python_docs.md](generate_python_docs.md)
- **Overview**: Scans specified directories for Python files and generates documentation using the OpenAI API.
- **Installation & Dependencies**: Requires Python 3.x and the `openai` library.
- **Usage Instructions**: Run the script in a terminal to generate documentation for found Python files.

---

## Hello World Script

A simple demonstration script that prints greetings to the console.

- **File**: [test_aniebiet.md](test_aniebiet.md)
- **Overview**: Illustrates basic output functionality in Python by greeting two individuals.
- **Installation & Dependencies**: No external dependencies; runs on Python 3.x.
- **Usage Instructions**: Write code to print greetings in a new Python file and execute it.

---

## Document Querying with PDF Input

Allows users to upload and query PDF documents using a Streamlit application.

- **File**: [deepseek_pdf_ui.md](OpenAI-DeepSeek-RAG/deepseek_pdf_ui.md)
- **Overview**: Processes PDF uploads, enables querying via LLM, and creates a vector index.
- **Installation & Dependencies**: Requires `streamlit`, `ipython`, `llama_index`, among others.
- **Usage Instructions**: Run the Streamlit application to interact with PDF documents.

---

## Document QA System

Implements a question-answering system for documents using embeddings.

- **File**: [openai_main.md](OpenAI-DeepSeek-RAG/openai_main.md)
- **Overview**: Loads markdown documents, generates embeddings, and allows queries for answers.
- **Installation & Dependencies**: Requires `python-dotenv`, `chromadb`, and `openai`.
- **Usage Instructions**: Execute the script after loading documents into the specified directory.

---

## Intelligent Document Query System (UTOM)

A Streamlit application for querying Markdown documents based on user input.

- **File**: [openai_ui.md](OpenAI-DeepSeek-RAG/openai_ui.md)
- **Overview**: Splits Markdown documents into chunks, generates embeddings, and allows querying.
- **Installation & Dependencies**: Requires `streamlit`, `python-dotenv`, and `openai`.
- **Usage Instructions**: Run the Streamlit application to query documents.

---

## GitHub API Fetcher

Interacts with the GitHub API to fetch repository details and issues.

- **File**: [github.md](RAGS/github.md)
- **Overview**: Fetches repository data, structures issues, and supports repository searches.
- **Installation & Dependencies**: Requires `requests`, `python-dotenv`, and `langchain-core`.
- **Usage Instructions**: Configure the GitHub token and run the script to fetch data.

---

## GitHub Repository Analyzer

An analyzer for searching and evaluating GitHub repositories.

- **File**: [github_repos.md](RAGS/github_repos.md)
- **Overview**: Fetches repository README files and computes semantic similarity with user context.
- **Installation & Dependencies**: Requires several `langchain` libraries alongside `requests` and `python-dotenv`.
- **Usage Instructions**: Execute the script with relevant search parameters.

---

## GitHub Issues and Repositories Inquiry Tool

Enables interaction with GitHub through a conversational interface.

- **File**: [issues.md](RAGS/issues.md)
- **Overview**: Allows users to query GitHub issues and repositories, utilizing Langchain and AstraDB.
- **Installation & Dependencies**: Requires various `langchain` libraries and setups for environment variables.
- **Usage Instructions**: Run the script and follow prompts to interact.

---

## Note Tool Script

A utility for saving text notes to a local file.

- **File**: [note.md](RAGS/note.md)
- **Overview**: Appends notes to a `notes.txt` file.
- **Installation & Dependencies**: Requires `langchain-core`.
- **Usage Instructions**: Call `note_tool` function with note content to save it.

---

## Chat with GitHub README Files

Facilitates interaction with GitHub repositories through their README files.

- **File**: [repo_flow.md](RAGS/repo_flow.md)
- **Overview**: Fetches repository data based on keywords and provides contextual analysis.
- **Installation & Dependencies**: Requires `requests`, `python-dotenv`, and various `langchain` libraries.
- **Usage Instructions**: Provide required input to the script for analysis.

--- 

This documentation provides a structured overview of the different components of the project. Each section references its respective file for detailed information, making it easier to navigate and understand the functionalities within the project.