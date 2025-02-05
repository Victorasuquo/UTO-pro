# GitHub Repository Semantic Analyzer with RAG Integration

This document provides a comprehensive overview of a Python script designed for searching GitHub repositories based on user-provided keywords, semantically analyzing their README files, and optionally integrating the results into a Retrieval-Augmented Generation (RAG) vector store using LangChain tools.

---

## Overview

The script performs the following key functions:

- **GitHub API Integration:**  
  Searches for repositories on GitHub using the provided query and fetches repository details and README files leveraging GitHub's API.

- **Semantic Analysis:**  
  Uses a Sentence Transformer model to compute the semantic similarity between a user-provided context and the content of each repository's README file.

- **Parallel Processing:**  
  Utilizes a thread pool executor to speed up the analysis of repositories.

- **Vector Store Integration (RAG):**  
  Connects to an AstraDB vector store and updates it with the matched repository information for further retrieval.

- **Interactive Q&A:**  
  Implements a question-answering loop using LangChain's agent executor to let users ask questions about the matched repositories.

---

## Installation & Dependencies

Before running the script, ensure you have the following dependencies installed:

- Python 3.7+
- Environment management with [python-dotenv](https://pypi.org/project/python-dotenv/)
- HTTP requests with [requests](https://docs.python-requests.org/)
- Sentence Transformer from [sentence-transformers](https://www.sbert.net/)
- LangChain modules:
  - langchain_core
  - langchain.agents
  - langchain_openai
  - langchain_astradb
  - langchain
- Concurrent execution using Python's built-in [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)

Installation example using pip:

```
pip install python-dotenv requests sentence-transformers langchain-core langchain openai langchain-astradb
```

Additionally, set up the following environment variables (possibly via a `.env` file):

- GITHUB_TOKEN: Your GitHub API token.
- ASTRA_DB_API_ENDPOINT: API endpoint for AstraDB.
- ASTRA_DB_APPLICATION_TOKEN: AstraDB token.
- ASTRA_DB_KEYSPACE: (Optional) Desired keyspace/namespace for AstraDB.

---

## Usage

1. **Run the Script:**  
   Execute the script in your terminal:
   ```
   python script_name.py
   ```

2. **Input Needed:**  
   - You will be prompted to enter keywords for the GitHub repository search.
   - Next, enter a context string that will be used to check similarity against repository README files.
   - After displaying matched repositories, you will be asked if you wish to update the RAG vector store.
   - Finally, you can ask questions about the repositories in an interactive loop (enter "q" to quit).

3. **Example Usage:**
   ```
   Enter keywords to search repositories: machine learning
   Enter the context to match in README files: deep learning model examples and tutorials
   Matched Repositories:
   1. repo_name (repo_owner)
      URL: https://github.com/repo_owner/repo_name
      Description: Repository for deep learning experiments.
      Similarity: 0.82
      README Snippet: <First 500 characters of the README>
   ---
   Do you want to update the RAG with matched repositories? (y/N): y
   Ask a question about matched repositories (q to quit): What is the repository about?
   [Agent output will be displayed]
   ```

---

## Function / Class Documentation

### fetch_github(owner, repo, endpoint)

- **Purpose:**  
  Fetches data from a specific GitHub repository endpoint using GitHub API.

- **Inputs:**
  - `owner` (str): The GitHub username or organization owning the repository.
  - `repo` (str): The name of the GitHub repository.
  - `endpoint` (str): The specific API endpoint (e.g., "readme").

- **Return Value:**  
  - (dict or None): JSON data from the API if the request is successful; otherwise, `None`.

---

### fetch_github_repositories(query, max_results=7)

- **Purpose:**  
  Searches for GitHub repositories that match the given query.

- **Inputs:**
  - `query` (str): Keywords to search for repositories.
  - `max_results` (int, optional): Maximum number of search results to return (default is 7).

- **Return Value:**  
  - (list): A list of repository items (dicts) returned by the GitHub search API. Returns an empty list on failure.

---

### fetch_readme(owner, repo)

- **Purpose:**  
  Retrieves and decodes the README file for a given GitHub repository.

- **Inputs:**
  - `owner` (str): The owner of the repository.
  - `repo` (str): Name of the repository.

- **Return Value:**  
  - (str): The decoded README content if available; otherwise, an empty string.

---

### analyze_repository(repo, context_embedding)

- **Purpose:**  
  Processes an individual repository by fetching its README, computing its semantic similarity to the provided context, and returning repository details if the similarity exceeds a threshold.

- **Inputs:**
  - `repo` (dict): Repository data from GitHub.
  - `context_embedding` (Tensor): The tokenized embedding of the user-provided context.

- **Return Value:**  
  - (dict or None): A dictionary containing repository information (name, owner, URL, description, a README snippet, and similarity score) if the semantic similarity is greater than 0.75; otherwise, `None`.

---

### analyze_repositories(query, context, max_results=7)

- **Purpose:**  
  Searches and semantically analyzes repositories based on the provided query and context.

- **Inputs:**
  - `query` (str): Search keywords for querying GitHub.
  - `context` (str): Context text to match against the repository README files.
  - `max_results` (int, optional): Maximum number of repositories to fetch (default is 7).

- **Return Value:**  
  - (list): A sorted list of repositories (dictionaries) that match the context, sorted by descending similarity score.

---

### display_matched_repositories(matched_repos)

- **Purpose:**  
  Prints out details of repositories that matched the semantic similarity search.

- **Inputs:**
  - `matched_repos` (list): A list of repository dictionaries that include details like name, owner, URL, description, similarity score, and README snippet.

- **Return Value:**  
  - None. Outputs details to the console.

---

### connect_to_vstore()

- **Purpose:**  
  Establishes a connection to an AstraDB vector store for RAG functionality using OpenAI embeddings.

- **Inputs:**  
  - None (relies on environment variables).

- **Return Value:**  
  - (AstraDBVectorStore object): An instance of the vector store ready for document operations.

---

## Code Walkthrough

1. **Environment Initialization:**  
   - Imports necessary libraries.
   - Loads environment variables using `load_dotenv()`.
   - Retrieves the GitHub token and AstraDB credentials from the environment variables.

2. **Model Initialization:**  
   - Initializes a Sentence Transformer model (`all-MiniLM-L6-v2`) for embedding text and computing semantic similarities.

3. **GitHub API Functions:**  
   - `fetch_github()`, `fetch_github_repositories()`, and `fetch_readme()` handle interactions with GitHub's API to fetch repository information and README content.

4. **Semantic Analysis:**  
   - `analyze_repository()` computes the similarity between a repository's README content and the provided context.
   - `analyze_repositories()` uses a thread pool executor to analyze multiple repositories concurrently, sorts them by similarity, and returns the matched repositories.

5. **Display Function:**  
   - `display_matched_repositories()` formats and prints the details of the matched repositories.

6. **Vector Store Connection:**  
   - `connect_to_vstore()` connects to an AstraDB instance configured for RAG functionality.
   - If the user opts to update the vector store, the script creates a list of `Document` objects from the README snippets and updates the vector store (deleting the existing collection if necessary).

7. **Interactive Agent Loop:**  
   - Sets up a retriever tool using LangChain.
   - Uses a language model agent to answer user queries about the matched repositories in a loop until the user quits.

---

## Example Output

After running the script, a sample output in the console might look like:

```
Enter keywords to search repositories: machine learning
Enter the context to match in README files: deep learning with Python
Matched Repositories:
1. ml_examples (johnDoe)
   URL: https://github.com/johnDoe/ml_examples
   Description: A repository containing machine learning examples.
   Similarity: 0.81
   README Snippet: "# ML Examples\nThis repo contains code examples..."
---
Do you want to update the RAG with matched repositories? (y/N): y
Ask a question about matched repositories (q to quit): What does ml_examples cover?
[Agent output based on the README snippet]
```

---

## Error Handling

- **GitHub API Requests:**  
  - Each GitHub API function checks the response status code.  
  - If a request fails (non-200), an error message is printed and a fallback value (`None` or empty list) is returned.

- **README Fetching:**  
  - If the README is not found or decoding fails, the function prints an appropriate error message.

- **Vector Store Update:**  
  - The update section attempts to delete the current collection in the vector store before inserting new documents.  
  - A bare exception is caught (with a simple `except:`), preventing the script from crashing if the deletion fails.

- **User Prompt Loop:**  
  - The interactive question-answering loop continues until the user enters "q", ensuring a graceful exit.

---

This detailed documentation should help you understand, configure, and extend the script as needed for GitHub repository analysis using semantic similarity and RAG integrations.