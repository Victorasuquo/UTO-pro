# Project Documentation Overview

This documentation provides a structured overview of the various markdown files included in the project. Each file serves a specific purpose related to project management workflows, documentation generation, API integration, and various utility scripts. The files are referenced below as clickable links pointing to their respective relative paths.

---

## Table of Contents

1. [General Project Documentation](#general-project-documentation)
2. [Documentation Generators & Automation](#documentation-generators--automation)
3. [Web Application & Project Workflow API](#web-application--project-workflow-api)
4. [Simple Script Examples](#simple-script-examples)
5. [PDF & Document Query Interfaces](#pdf--document-query-interfaces)
6. [GitHub API and Repository Analysis Tools](#github-api-and-repository-analysis-tools)
7. [Note Taking Utility](#note-taking-utility)

---

## General Project Documentation

- **[3o_mini.md](3o_mini.md)**  
  Provides an organized summary of the project's markdown files, including an overview table of contents that lists all available documents and their purposes.

- **[GENERAL_DOCUMENTATION.md](GENERAL_DOCUMENTATION.md)**  
  Acts as a master index for the project files. It outlines the purpose of each document residing in the repository with clickable relative paths for easy navigation.

- **[Readme.md](Readme.md)**  
  Offers detailed instructions and an overview of the project workflow. This file explains the setup for a Flask application that leverages MongoDB and OpenAI’s GPT model for managing project-related tasks.

- **[OpenAI-DeepSeek-RAG/files/Readme.md](OpenAI-DeepSeek-RAG/files/Readme.md)**  
  Another variant of the README that describes a Flask-based API project workflow, similar to the root-level README, but specific to files within the OpenAI-DeepSeek-RAG directory.

---

## Documentation Generators & Automation

- **[generate_python_docs.md](generate_python_docs.md)**  
  Describes a Python script that generates structured Markdown documentation for Python source files. It uses the OpenAI API and multiprocessing to scan directories, document code, and output Markdown files alongside the source code.

- **[gen_docs_generator 3o model.md](gen_docs_generator 3o model.md)**  
  Documents a Python script that generates documentation for Markdown files in a given directory. It includes details on how the script recursively searches for `.md` files, reads them, and generates comprehensive documentation using OpenAI’s ChatCompletion API. The output is saved as `3o_mini.md`.

- **[gen_docs_generator.md](gen_docs_generator.md)**  
  Similar to the previous generator, this file details the process of creating structured documentation from markdown files by reading content, handling encoding issues, and leveraging multiprocessing with OpenAI API calls. The final output is written into `GENERAL_DOCUMENTATION.md`.

---

## Web Application & Project Workflow API

- **[endpoint_.md](endpoint_.md)**  
  Provides detailed API documentation for a Flask-based web service used in project workflow automation. It explains endpoints, integration with MongoDB, usage of OpenAI's GPT model, installation steps, and error handling.

---

## Simple Script Examples

- **[test_aniebiet.md](test_aniebiet.md)**  
  Contains documentation for a simple Python script that prints two greeting messages. This script demonstrates basic usage of the `print()` function and serves as an example of a minimal, standalone Python script.

---

## PDF & Document Query Interfaces

- **[OpenAI-DeepSeek-RAG/deepseek_pdf_ui.md](OpenAI-DeepSeek-RAG/deepseek_pdf_ui.md)**  
  Documents a Python script that creates a Streamlit-powered web interface for querying PDF documents. The interface uses LlamaIndex for processing, a HuggingFace embedding model, and an LLM via Ollama for answering questions about the content of uploaded PDFs.

- **[OpenAI-DeepSeek-RAG/openai_main.md](OpenAI-DeepSeek-RAG/openai_main.md)**  
  Explains a Python script designed to perform document QA by splitting markdown files, generating embeddings with the OpenAI API, storing them in a persistent Chroma database, and querying the database to generate responses using a ChatGPT-like API.

- **[OpenAI-DeepSeek-RAG/openai_ui.md](OpenAI-DeepSeek-RAG/openai_ui.md)**  
  Provides comprehensive documentation for the "UTOM: Intelligent Document Query System". This system uses Streamlit for the UI, integrates with a vector store (ChromaDB) for document embeddings, and uses the OpenAI API to generate chat responses based on user queries.

---

## GitHub API and Repository Analysis Tools

- **[RAGS/github.md](RAGS/github.md)**  
  Details a Python script that interacts with GitHub’s API to fetch repository data and issues. It explains the process of converting GitHub issues into a standardized document format for further processing.

- **[RAGS/github_repos.md](RAGS/github_repos.md)**  
  Documents a tool that searches GitHub repositories using provided keywords, analyzes README files for semantic similarity against a given context, and integrates the data into a Retrieval-Augmented Generation (RAG) system.

- **[RAGS/github_search.md](RAGS/github_search.md)**  
  Provides an overview of a script that semantically analyzes GitHub repositories. The script fetches repository details and README contents, computes semantic similarity, and optionally integrates the results into a RAG vector store using LangChain.

- **[RAGS/issues.md](RAGS/issues.md)**  
  Describes a GitHub Issues and Repository Search & Update Tool. This CLI-based script allows users to search for repositories or ask questions related to GitHub issues using an underlying agent coupled with a vector store backed by AstraDB.

- **[RAGS/repo.md](RAGS/repo.md)**  
  Offers detailed documentation for a GitHub Repository Analyzer. The script interacts with the GitHub API to search for repositories, fetch their README contents, and display repositories that match a specified context.

- **[RAGS/repo_flow.md](RAGS/repo_flow.md)**  
  Documents a RAG-powered tool that analyzes GitHub repositories. The script searches for repositories, examines README files for relevant context, and updates an AstraDB vector store for interactive querying via a tool-calling agent.

---

## Note Taking Utility

- **[RAGS/note.md](RAGS/note.md)**  
  Provides documentation for a simple Note Saver Tool. This Python script appends user-provided text notes to a local file ("notes.txt"). It outlines installation steps, usage examples, and details on how the tool leverages the `langchain_core` library.

---

This documentation file serves as a centralized guide to understand the role of each markdown file in the project. Each file description includes clickable relative paths for easy navigation, enabling developers and users alike to quickly locate and utilize the relevant documentation and tools within the project repository.