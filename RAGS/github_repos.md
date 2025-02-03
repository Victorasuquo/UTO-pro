# GitHub Repository Analyzer

## Overview
This script analyzes GitHub repositories based on specified search queries and contexts. It utilizes the GitHub API to fetch repositories, their README files, and computes semantic similarity between the README content and the provided context using a sentence transformer model. It also allows users to connect to a database to store results, and it includes functionality to generate a README.md file for the matched repository.

## Installation & Dependencies
To run this script, please ensure you have the following dependencies installed:

- `requests`
- `python-dotenv`
- `langchain-core`
- `langchain-agents`
- `langchain-tools`
- `langchain-openai`
- `langchain-astraDB`
- `sentence-transformers`
- `concurrent.futures`

You can install the required packages using pip:

```bash
pip install requests python-dotenv langchain-core langchain-agents langchain-tools langchain-openai langchain-astraDB sentence-transformers
```

Additionally, make sure to set your GitHub token and other required environment variables in a `.env` file:

```plaintext
GITHUB_TOKEN=your_github_token
ASTRA_DB_API_ENDPOINT=your_astra_db_api_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_application_token
ASTRA_DB_KEYSPACE=your_desired_namespace
```

## Usage
To run the script, you can execute it from the command line:

```bash
python script_name.py
```

It will prompt for:
1. A search query to look for repositories.
2. Context that needs to be matched in the README files.

```plaintext
Enter keywords to search repositories: <your_search_keywords>
Enter the context to match in README files: <your_context>
```

Once the analysis completes, it will display the matched repositories and ask if you want to update the RAG (Retrieval-Augmented Generation) with matched repositories.

## Function/Class Documentation

### `fetch_github(owner: str, repo: str, endpoint: str) -> dict`
- **Purpose**: Fetch data from a specific GitHub endpoint for a given repository.
- **Input Parameters**:
  - `owner` (str): The owner of the repository.
  - `repo` (str): The name of the repository.
  - `endpoint` (str): The API endpoint to fetch (e.g., "readme").
- **Return Values**:
  - `dict`: The JSON response from the GitHub API or None if the request fails.

### `fetch_github_repositories(query: str, max_results: int = 7) -> list`
- **Purpose**: Search GitHub repositories based on a specified query.
- **Input Parameters**:
  - `query` (str): Search query for repositories.
  - `max_results` (int, optional): Maximum number of results to return. Default is 7.
- **Return Values**:
  - `list`: A list of repositories that match the search query.

### `fetch_readme(owner: str, repo: str) -> str`
- **Purpose**: Fetch the README file content for a specified repository.
- **Input Parameters**:
  - `owner` (str): The owner of the repository.
  - `repo` (str): The name of the repository.
- **Return Values**:
  - `str`: The content of the README file or an empty string if not found.

### `analyze_repository(repo: dict, context_embedding: tensor) -> dict`
- **Purpose**: Analyze a repository against the context embedding for semantic similarity.
- **Input Parameters**:
  - `repo` (dict): Repository details fetched from GitHub.
  - `context_embedding` (tensor): The semantic embedding of the input context.
- **Return Values**:
  - `dict`: Details of the repository if it matches the similarity threshold, otherwise None.

### `analyze_repositories(query: str, context: str, max_results: int = 7) -> list`
- **Purpose**: Analyze multiple repositories to match with the provided context.
- **Input Parameters**:
  - `query` (str): Search query for repositories.
  - `context` (str): Context against which the repositories should be matched.
  - `max_results` (int, optional): Maximum results to analyze. Default is 7.
- **Return Values**:
  - `list`: Sorted list of matched repositories based on similarity.

### `display_matched_repositories(matched_repos: list) -> None`
- **Purpose**: Print the details of matched repositories.
- **Input Parameters**:
  - `matched_repos` (list): List of repositories matched with the context.
- **Return Values**: None.

### `connect_to_vstore() -> AstraDBVectorStore`
- **Purpose**: Establish a connection to the AstraDB vector store.
- **Input Parameters**: None.
- **Return Values**:
  - `AstraDBVectorStore`: An instance of the vector store.

### `generate_readme(repository: dict, context: str) -> None`
- **Purpose**: Generate a README.md file for the top matched repository.
- **Input Parameters**:
  - `repository` (dict): The matched repository data.
  - `context` (str): The context used for the analysis.
- **Return Values**: None.

## Code Walkthrough
1. **Environment Setup**: Load required environment variables (e.g., GitHub token, AstraDB configs).
2. **Model Initialization**: Initialize the `SentenceTransformer` model for semantic similarity analysis.
3. **Function Definitions**: Several functions are defined to interact with GitHub API and internal logic for analyzing repositories.
4. **Main Execution Block**:
   - Capture user input for repository search and context.
   - Invoke functions to analyze repositories based on the input.
   - Display matched repositories and handle updates to the vector store.
   - Prompt for generating README.md for the top matched repository.

## Example Output
When the script is executed successfully, it may display outputs such as:

```plaintext
Matched Repositories:
1. awesome-python (sindresorhus)
   URL: https://github.com/sindresorhus/awesome
   Description: A curated list of awesome Python frameworks, libraries...
   Similarity: 0.82
   README Snippet: A curated list of awesome Python frameworks, libraries...
---
```

## Error Handling
- Each function that interacts with the GitHub API checks the `response.status_code` to validate the response. If the response does not indicate success (status code 200), it prints an error message and returns a default value (None or empty list).
- When attempting to delete the vector store collection, the code is wrapped in a `try-except` block to gracefully handle any potential errors.