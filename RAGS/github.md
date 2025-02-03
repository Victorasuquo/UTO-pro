# GitHub API Fetcher

## Overview
The **GitHub API Fetcher** is a Python script that interacts with the GitHub API to fetch repository details and issues for specified GitHub repositories. The script supports retrieving issues, loading and structuring issue data into documents, and searching for repositories based on a query.

## Installation & Dependencies
To run this script, ensure you have the following dependencies installed:
- `requests` for making HTTP requests.
- `python-dotenv` for loading environment variables from a `.env` file.
- `langchain-core` for handling document structures.

### Installation Steps
Install the required packages using pip:
```bash
pip install requests python-dotenv langchain-core
```

### Environmental Setup
Create a `.env` file in the same directory as the script with the following content:
```
GITHUB_TOKEN=your_personal_access_token
```
Replace `your_personal_access_token` with a valid GitHub Personal Access Token.

## Usage
To use the script, run it in a Python environment after ensuring that the required packages are installed and environment variables are set.

Here's an example of how to call the functions defined in the script:
```python
# Fetch issues from a specific GitHub repository
issues = fetch_github_issues("owner_name", "repo_name")

# Search for repositories with a specific query
repositories = fetch_github_repositories("search_query")
```

## Function/Class Documentation

### `fetch_github(owner: str, repo: str, endpoint: str) -> list`
- **Purpose**: Fetch data from a specified GitHub repository endpoint.
- **Input Parameters**:
  - `owner` (str): The GitHub username or organization that owns the repository.
  - `repo` (str): The name of the repository.
  - `endpoint` (str): The API endpoint to fetch data from (e.g., "issues").
- **Return Value**:
  - (list): A list of JSON objects returned from the API, or an empty list if the request fails.

### `fetch_github_issues(owner: str, repo: str) -> list`
- **Purpose**: Fetch issues from a specified GitHub repository.
- **Input Parameters**:
  - `owner` (str): The GitHub username or organization that owns the repository.
  - `repo` (str): The name of the repository.
- **Return Value**:
  - (list): A list of structured issue documents.

### `fetch_github_repositories(query: str, max_results: int = 5) -> list`
- **Purpose**: Search for GitHub repositories based on a query.
- **Input Parameters**:
  - `query` (str): The search term for querying repositories.
  - `max_results` (int, optional): The maximum number of repository results to return (default is 5).
- **Return Value**:
  - (list): A list of found repositories according to the search term.

### `load_issues(issues: list) -> list`
- **Purpose**: Transform the list of issues into structured document objects.
- **Input Parameters**:
  - `issues` (list): A list of raw issue data from the GitHub API.
- **Return Value**:
  - (list): A list of `Document` objects containing formatted issue data.

## Code Walkthrough
1. **Module Imports**:
    - The script begins with importing necessary modules, including `os`, `requests`, `load_dotenv`, and the `Document` class from `langchain_core`.
    
2. **Loading Environment Variables**:
    - The `load_dotenv()` function is invoked to load the GitHub token from a `.env` file.

3. **Defining `fetch_github`**:
    - This function constructs the API URL, sets the authorization headers, and makes a GET request to the specified endpoint. It checks for a successful response and returns the data or an empty list if an error occurs.

4. **Defining `fetch_github_issues`**:
    - This function calls `fetch_github` with the "issues" endpoint to retrieve issues for a specific repository.

5. **Defining `fetch_github_repositories`**:
    - Similar to `fetch_github`, this function constructs a URL for searching repositories and returns a list of found repositories or an empty list.

6. **Defining `load_issues`**:
    - This function processes the raw issue data, extracts relevant metadata, and creates a list of `Document` objects that structure the issue content.

## Example Output
When calling the `fetch_github_issues` function, the output would be a list of documents representing issues. Each document would contain the title and body of the issue along with its metadata such as author and created date.

## Error Handling
The script includes basic error handling by checking the response status code from the GitHub API calls. If a request fails (i.e., status code is not 200), the script prints an error message indicating the failure and returns an empty list instead of raising an exception. This allows for graceful failure handling during API interactions.