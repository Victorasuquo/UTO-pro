# Documentation for Python Script: Chat with GitHub README Files

## Overview
This script enables users to search for GitHub repositories based on a given keyword query and context, fetches their README files, and performs a context-based analysis. It utilizes the Langchain library for retrieval-augmented generation (RAG) functionalities, allowing users to ask questions regarding the matched repositories.

## Installation & Dependencies
To run this script, you need the following dependencies:
- `requests`
- `python-dotenv`
- `langchain`
- `langchain-openai`
- `langchain-astradb`

You can install these dependencies via pip:
```bash
pip install requests python-dotenv langchain langchain-openai langchain-astradb
```

Additionally, ensure you have the following environment variables set:
- `GITHUB_TOKEN`: Personal access token for GitHub API access.
- `ASTRA_DB_API_ENDPOINT`: API endpoint for Astra DB.
- `ASTRA_DB_APPLICATION_TOKEN`: Application token for Astra DB access.
- `ASTRA_DB_KEYSPACE`: Keyspace in Astra DB.

## Usage
To run the script, execute it in a Python environment:
```bash
python script_name.py
```

### Input Prompts
1. Enter keywords to search repositories.
2. Enter the context to match in README files.
3. Optionally, choose whether to update the AstraDB vector store with matched repositories.
4. Ask questions about the matched repositories until you type 'q' to quit.

## Function/Class Documentation

### Function: `fetch_github(owner: str, repo: str, endpoint: str) -> dict`
- **Purpose**: Fetch data from a specified endpoint of a GitHub repository.
- **Input Parameters**:
  - `owner` (str): GitHub username or organization name.
  - `repo` (str): GitHub repository name.
  - `endpoint` (str): Specific API endpoint to target.
- **Return Values**: 
  - Returns a dictionary containing the response data if successful.
  - Returns `None` on failure.

### Function: `fetch_github_repositories(query: str, max_results: int = 7) -> list`
- **Purpose**: Search for repositories based on a keyword query.
- **Input Parameters**:
  - `query` (str): Search keywords.
  - `max_results` (int): Maximum number of repositories to fetch (default is 7).
- **Return Values**:
  - Returns a list of repository dictionaries if successful.
  - Returns an empty list on failure.

### Function: `fetch_readme(owner: str, repo: str) -> str`
- **Purpose**: Retrieve the README file content for a specific repository.
- **Input Parameters**:
  - `owner` (str): GitHub username or organization name.
  - `repo` (str): GitHub repository name.
- **Return Values**: 
  - Returns the README content as a string if successful.
  - Returns an empty string if no README is found.

### Function: `analyze_repositories(query: str, context: str, max_results: int = 7) -> list`
- **Purpose**: Analyze GitHub repositories based on the search query and README context.
- **Input Parameters**:
  - `query` (str): Search keywords.
  - `context` (str): Context to look for in the README files.
  - `max_results` (int): Maximum number of repositories to analyze.
- **Return Values**: 
  - Returns a list of matched repository dictionaries.

### Function: `display_matched_repositories(matched_repos: list) -> None`
- **Purpose**: Display matched repositories and their details.
- **Input Parameters**:
  - `matched_repos` (list): List of matched repository dictionaries.
- **Return Values**: None.

### Function: `connect_to_vstore() -> AstraDBVectorStore`
- **Purpose**: Establish a connection with the Astra DB vector store.
- **Input Parameters**: None.
- **Return Values**: Returns an instance of `AstraDBVectorStore`.

## Code Walkthrough
1. **Environment Setup**: Load environment variables using `dotenv`.
2. **Fetching Data**:
   - The `fetch_github` function retrieves data from GitHub.
   - The `fetch_github_repositories` function queries GitHub for repositories matching a search term.
   - The `fetch_readme` function fetches the README content for a repository.
3. **Analyzing Repositories**:
   - The `analyze_repositories` function collects repositories and checks for the specified context in their README.
4. **Displaying Results**:
   - The `display_matched_repositories` function prints out matched repositories to the console.
5. **Storing Data**:
   - Connects to an Astra DB vector store and potentially updates it with matched repository data.
6. **Interactive Query**:
   - Prompts the user for questions about the matched repositories, using a Langchain agent to generate responses.

## Example Output
Upon successful execution, the console output would look similar to this:
```
Matched Repositories:
1. repo_name (repo_owner)
   URL: https://github.com/owner/repo_name
   Description: A brief description of the repository.
   README Snippet: Here is a short snippet of the README content...
---
```

## Error Handling
- The script includes basic error handling for HTTP requests, printing out error messages if the requests fail.
- The `connect_to_vstore` function contains error handling for potential issues when deleting collections in the vector store.
  
This documentation outlines the functionality and usage of the script focused on RAG interactions with GitHub README files, providing clear instructions and a detailed overview of the components involved.