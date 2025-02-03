# GitHub Repository Analyzer

## Overview
The GitHub Repository Analyzer script fetches and analyzes repositories from GitHub based on user-provided search queries and context. It computes semantic similarity between the README files of the retrieved repositories and the specified context. The script also connects to a vector store for information retrieval augmented generation (RAG) functionality, allowing users to ask questions about the repositories using a natural language interface.

## Installation & Dependencies
To run the GitHub Repository Analyzer, you need the following dependencies and environment setup:

- Python 3.x
- Required packages:
  - `requests`
  - `python-dotenv`
  - `sentence-transformers`
  - `langchain`
  - `langchain_openai`
  - `langchain_astradb`
  
### Install dependencies using pip:
```bash
pip install requests python-dotenv sentence-transformers langchain langchain_openai langchain_astradb
```

### Environment Variables:
Before running the script, ensure you have the following environment variables set:
- `GITHUB_TOKEN`: Your GitHub Personal Access Token.
- `ASTRA_DB_API_ENDPOINT`: Endpoint for Astra DB API.
- `ASTRA_DB_APPLICATION_TOKEN`: Application token for Astra DB.
- `ASTRA_DB_KEYSPACE`: The desired namespace for the Astra DB.

## Usage
To run the script, execute the following command in your terminal:
```bash
python your_script_name.py
```

The script will prompt you for:
1. Keywords to search repositories.
2. The context to match in README files.

## Function/Class Documentation

### `fetch_github(owner: str, repo: str, endpoint: str) -> dict`
- **Purpose**: Fetches data from a specified GitHub repository endpoint.
- **Parameters**:
  - `owner` (str): The owner of the repository.
  - `repo` (str): The name of the repository.
  - `endpoint` (str): The specific endpoint to fetch.
- **Returns**: `dict` containing the repository data or `None` if the request fails.

### `fetch_github_repositories(query: str, max_results: int = 7) -> list`
- **Purpose**: Searches for repositories on GitHub based on a query string.
- **Parameters**:
  - `query` (str): The search query for repositories.
  - `max_results` (int): The maximum number of repositories to return (default is 7).
- **Returns**: `list` of repositories or an empty list if the request fails.

### `fetch_readme(owner: str, repo: str) -> str`
- **Purpose**: Fetches the README content for a specified repository.
- **Parameters**:
  - `owner` (str): The owner of the repository.
  - `repo` (str): The name of the repository.
- **Returns**: `str` containing the README content or an empty string if not found.

### `analyze_repository(repo: dict, context_embedding: Any) -> dict`
- **Purpose**: Analyzes a single repository by comparing its README content with the context embedding.
- **Parameters**:
  - `repo` (dict): Dictionary containing repository details.
  - `context_embedding` (Any): The context embedding to compare against.
- **Returns**: `dict` with repository information and similarity score or `None` if below the similarity threshold.

### `analyze_repositories(query: str, context: str, max_results: int = 7) -> list`
- **Purpose**: Analyzes multiple repositories based on a search query and context.
- **Parameters**:
  - `query` (str): The search query for repositories.
  - `context` (str): The context to be matched in README files.
  - `max_results` (int): The maximum number of repositories to analyze (default is 7).
- **Returns**: `list` of matched repositories sorted by similarity.

### `display_matched_repositories(matched_repos: list)`
- **Purpose**: Displays the information of matched repositories to the console.
- **Parameters**:
  - `matched_repos` (list): List of matched repository dictionaries.
- **Returns**: None.

### `connect_to_vstore() -> AstraDBVectorStore`
- **Purpose**: Connects to the Astra DB vector store for storing and retrieving documents.
- **Parameters**: None.
- **Returns**: An instance of `AstraDBVectorStore`.

## Code Walkthrough

1. **Import Statements**: The script imports necessary modules for HTTP requests, environment variables, semantic analysis, and vector store connections.
2. **Environment Setup**: Loads environment variables using `load_dotenv()` and retrieves the GitHub token.
3. **Model Initialization**: Initializes a pre-trained SentenceTransformer model for semantic similarity.
4. **Function Definitions**: Contains several functions for fetching data from GitHub, analyzing repositories, and connecting to the vector store.
5. **Main Execution Block**: Prompts user for search query and context, analyzes repositories, displays results, and optionally connects to a vector store to update it with matched repositories.
6. **Natural Language Processing**: Utilizes an agent to facilitate question-answering regarding matched repositories.

## Example Output
When executed properly, the script provides output in the following format:
```
Matched Repositories:
1. example-repo (username)
   URL: https://github.com/username/example-repo
   Description: A brief description of the repository
   Similarity: 0.85
   README Snippet: This is a snippet of the README file...
---
```

## Error Handling
The script includes basic error handling by checking HTTP response statuses when fetching data from GitHub. In case of a failure, it prints an error message with the failed status code. Additionally, when updating the vector store, it attempts to delete an existing collection, suppressing exceptions if the collection does not exist. 

Overall, the script aims to gracefully handle user input and unexpected API behaviors while providing meaningful output.