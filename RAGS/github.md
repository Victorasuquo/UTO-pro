# GitHub API Utility Script Documentation

This document provides detailed information about the Python script that interacts with GitHub’s API to fetch repositories and issues, then process the issues into document objects.

---

## Overview

This script offers utility functions to:
- Fetch data from GitHub API endpoints.
- Retrieve a list of issues for a repository.
- Search for repositories using a query.
- Convert GitHub issue data into a standardized document format using the `Document` class from `langchain_core.documents`.

The script leverages environment variables for securing the GitHub token and uses external libraries to aid HTTP requests and environment configuration.

---

## Installation & Dependencies

Before running the script, ensure the following dependencies are installed:

- [Python 3.x](https://www.python.org)
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [langchain_core](https://pypi.org/project/langchain-core/) (or ensure the corresponding module is accessible)

You can install the necessary Python packages using pip:

```bash
pip install requests python-dotenv langchain_core
```

Additionally, create a `.env` file in your project directory with the following content, replacing `<YOUR_GITHUB_TOKEN>` with your actual GitHub token:

```env
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
```

---

## Usage

Run the script by executing it from the command line or by importing its functions in another Python project. For example:

```bash
python script_name.py
```

To use this script as a module, you can import and call its functions:

```python
from script_name import fetch_github_issues, fetch_github_repositories

# Fetch issues for a specific repository
issues = fetch_github_issues("owner_name", "repository_name")

# Search for repositories matching a query
repositories = fetch_github_repositories("machine learning")
```

---

## Function and Class Documentation

### 1. Function: fetch_github

**Purpose:**  
Fetch data from a specified GitHub repository endpoint.

**Input Parameters:**
- `owner` (str): The GitHub username or organization that owns the repository.
- `repo` (str): The name of the GitHub repository.
- `endpoint` (str): The API endpoint to query (e.g., `"issues"`).

**Returns:**  
- (list or dict): Returns the JSON data response if the request is successful. In the event of a failure, an empty list is returned.

**Example Usage:**

```python
data = fetch_github("octocat", "Hello-World", "issues")
```

---

### 2. Function: fetch_github_issues

**Purpose:**  
Retrieve GitHub issues from a specific repository by calling the `fetch_github` function with the "issues" endpoint.

**Input Parameters:**
- `owner` (str): The GitHub username or organization that owns the repository.
- `repo` (str): The name of the GitHub repository.

**Returns:**  
- (list): A list of issues data obtained from GitHub.

**Example Usage:**

```python
issues = fetch_github_issues("octocat", "Hello-World")
```

---

### 3. Function: fetch_github_repositories

**Purpose:**  
Search for GitHub repositories based on a query string.

**Input Parameters:**
- `query` (str): The search query to filter repositories.
- `max_results` (int, optional): The maximum number of repository results to return (default is 5).

**Returns:**  
- (list): A list of repository items extracted from the GitHub search results. If the API call fails, an empty list is returned.

**Example Usage:**

```python
repos = fetch_github_repositories("machine learning", max_results=10)
```

---

### 4. Function: load_issues

**Purpose:**  
Convert raw GitHub issue data into a list of `Document` objects, each containing the issue’s content and associated metadata.

**Input Parameters:**
- `issues` (list): A list of GitHub issue dictionaries retrieved from the API.

**Returns:**  
- (list): A list of `Document` objects with the following details:
  - **page_content** (str): A concatenated string made from the issue title and body.
  - **metadata** (dict): Contains:
    - `author` (str): The GitHub user login of the issue creator.
    - `comments` (int): The number of comments on the issue.
    - `body` (str): The body of the issue.
    - `labels` (list): A list of labels associated with the issue.
    - `created_at` (str): The creation timestamp of the issue.

**Example Usage:**

```python
docs = load_issues(issues)
```

---

## Code Walkthrough

1. **Imports and Environment Setup:**
   - The script imports required modules:
     - `os` for environment variables.
     - `requests` for HTTP requests.
     - `load_dotenv` from `dotenv` to load environment variables from a `.env` file.
     - `Document` from `langchain_core.documents` for document creation.
   - `load_dotenv()` loads environment variables, including `GITHUB_TOKEN`, from a `.env` file.

2. **Authentication:**
   - The GitHub token is fetched from the environment using:
     ```python
     github_token = os.getenv("GITHUB_TOKEN")
     ```

3. **Function: fetch_github:**
   - Constructs the API URL using formatted strings.
   - Adds an authorization header with the GitHub token.
   - Executes a GET request to GitHub API.
   - If successful (`response.status_code == 200`), returns parsed JSON data; otherwise, prints an error message and returns an empty list.

4. **Function: fetch_github_issues:**
   - Specifically queries the "issues" endpoint by calling `fetch_github` with "issues".

5. **Function: fetch_github_repositories:**
   - Searches for repositories using GitHub’s search API.
   - Sends a GET request with appropriate headers and query parameters (`q` for query and `per_page` for maximum results).
   - Extracts and returns repository items from the search results. In case of error, an empty list is returned.

6. **Function: load_issues:**
   - Iterates over the list of issues.
   - For each issue, constructs a metadata dictionary containing author, comment count, issue body, labels, and creation time.
   - Concatenates the title and body of the issue to form document content.
   - Creates a `Document` object for each issue and appends it to a list.
   - Finally, returns a list of document objects.

---

## Example Output

If you run the function `fetch_github_repositories("langchain")`, the output might look like:

```json
{
  "id": 123456,
  "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY=",
  "name": "langchain",
  "full_name": "owner/langchain",
  "private": false,
  // additional repository details...
}
```

For `fetch_github_issues("octocat", "Hello-World")`, you may see a list of issues in a similar JSON structure, which are later processed into Document objects.

---

## Error Handling

- The script checks the response status code after each API call:
  - If the status code is 200, the response JSON is processed.
  - If not, an error message with the status code is printed, and the function returns an empty list.
- This approach ensures the program does not break abruptly during an API failure, allowing users to handle empty responses gracefully.

---

This detailed documentation should help you understand, install, and utilize the GitHub API utility script effectively.