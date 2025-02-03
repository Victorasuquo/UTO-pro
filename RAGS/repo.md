# GitHub Repository Analyzer

## Overview
The GitHub Repository Analyzer is a Python script that facilitates the search and analysis of repositories on GitHub. It allows users to search for repositories based on specific keywords and contexts, fetches relevant README files, and displays a summary of matched repositories.

## Installation & Dependencies
To run this script, ensure you have the following dependencies installed:

- `requests`: To make HTTP requests to the GitHub API.
- `python-dotenv`: To load environment variables from a `.env` file.
- `langchain_core`: Required for document handling (though not explicitly utilized in this script).

You can install the required dependencies using pip:
```bash
pip install requests python-dotenv langchain_core
```

Additionally, ensure that you have a GitHub token for authentication. Store your GitHub token in a `.env` file as follows:
```
GITHUB_TOKEN=your_github_token_here
```

## Usage
To use the script, run it and provide the required inputs when prompted. The script will search for repositories and display matched results based on the provided context.

### Example
```bash
python github_analyzer.py
```
- When prompted, enter a search query (e.g., `machine learning`).
- Enter the context to match in README files (e.g., `neural networks`).

## Function/Class Documentation

### `fetch_github(owner: str, repo: str, endpoint: str) -> dict`
Fetches data from a specified GitHub repository endpoint.

- **Parameters:**
  - `owner` (str): The GitHub username or organization name owning the repository.
  - `repo` (str): The repository name.
  - `endpoint` (str): The specific GitHub API endpoint to fetch data from.
  
- **Returns:**
  - `dict`: JSON response from the GitHub API if successful; otherwise, `None`.

---

### `fetch_github_repositories(query: str, max_results: int = 7) -> list`
Searches for GitHub repositories based on a query string.

- **Parameters:**
  - `query` (str): The search keywords for locating repositories.
  - `max_results` (int, optional): Maximum number of results to retrieve (default is 7).
  
- **Returns:**
  - `list`: List of repositories matching the search query.

---

### `fetch_readme(owner: str, repo: str) -> str`
Fetches the README file content of a specified repository.

- **Parameters:**
  - `owner` (str): The GitHub username or organization name owning the repository.
  - `repo` (str): The repository name.

- **Returns:**
  - `str`: Decoded content of the README file if found; otherwise, an empty string.

---

### `analyze_repositories(query: str, context: str, max_results: int = 7) -> list`
Analyzes repositories based on a search query and context, matching the context within README files.

- **Parameters:**
  - `query` (str): The search keywords for locating repositories.
  - `context` (str): The context to match in README content.
  - `max_results` (int, optional): Maximum number of results to analyze (default is 7).
  
- **Returns:**
  - `list`: List of matched repositories with their details.

---

### `display_matched_repositories(matched_repos: list)`
Displays the matched repository information on the console.

- **Parameters:**
  - `matched_repos` (list): List of matched repositories information.

## Code Walkthrough
1. **Loading Environment Variables**: The script begins by loading environment variables from a `.env` file which contains the GitHub token.
   
2. **Fetch GitHub Functionality**: The `fetch_github` function retrieves data from the specified GitHub API endpoint and checks for a successful response.

3. **Repository Search**: The `fetch_github_repositories` function is called to search GitHub repositories based on user input.

4. **Fetching README Files**: For each matched repository, the `fetch_readme` function retrieves the README content. The README is decoded from base64 format.

5. **Analyzing Contexts**: The `analyze_repositories` function compares the context with the README contents and gathers matched repositories.

6. **Displaying Results**: The `display_matched_repositories` function outputs the matching repositories in a user-friendly format.

## Example Output
After running the script and providing the inputs, the output may look like:
```
Matched Repositories:
1. repo_name_1 (owner_name)
   URL: https://github.com/owner_name/repo_name_1
   Description: A brief description of the repository.
   README Snippet: This is a snippet of the README file...
---
2. repo_name_2 (owner_name)
   URL: https://github.com/owner_name/repo_name_2
   Description: Another repository description.
   README Snippet: Here is another part of the README...
```

## Error Handling
- The script includes basic error handling for API requests. If the request fails (i.e., does not return a 200 status code), an error message is printed indicating the failure reason.
- The `fetch_readme` function handles cases where no README content is found and returns an empty string.