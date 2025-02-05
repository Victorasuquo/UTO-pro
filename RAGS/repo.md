# Python GitHub Repository Analyzer Documentation

This documentation provides an in-depth explanation of the Python script that interacts with the GitHub API to search repositories, fetch README contents, and match repositories based on a given context. The script uses environment variables for authentication and outputs repository details if they contain a specified context string in their README files.

---

## Table of Contents

- [Overview](#overview)
- [Installation & Dependencies](#installation--dependencies)
- [Usage](#usage)
- [Function Documentation](#function-documentation)
  - [fetch_github](#fetch_github)
  - [fetch_github_repositories](#fetch_github_repositories)
  - [fetch_readme](#fetch_readme)
  - [analyze_repositories](#analyze_repositories)
  - [display_matched_repositories](#display_matched_repositories)
- [Code Walkthrough](#code-walkthrough)
- [Example Output](#example-output)
- [Error Handling](#error-handling)

---

## Overview

The script facilitates the following tasks:

- **GitHub API Interaction:** It connects to the GitHub API using a personal access token.
- **Repository Search:** It searches GitHub repositories based on a user-defined keyword query.
- **README Analysis:** It fetches the README file from each repository and checks if a specific context string is present.
- **Result Display:** It outputs matched repositories with details such as owner, repository name, URL, description, and a snippet of the README.

---

## Installation & Dependencies

Before running the script, ensure that the following dependencies are installed:

- Python 3.x
- [requests](https://pypi.org/project/requests/) - For making HTTP requests.
- [python-dotenv](https://pypi.org/project/python-dotenv/) - For loading environment variables from a `.env` file.
- [langchain_core.documents](#) - (Assumed to be installed, check your package manager or repository for details)

To install dependencies, you can use pip:

```bash
pip install requests python-dotenv
```

Make sure you have a `.env` file in the script's directory containing your GitHub token:

```bash
GITHUB_TOKEN=your_github_token_here
```

---

## Usage

Run the script from the command line. The script will prompt you to enter a search query and a context string to match in the README files.

Example:

```bash
python script.py
```

When prompted:
- Enter keywords for repository search (e.g., "machine learning").
- Enter the context string to look for in README files (e.g., "TensorFlow").

---

## Function Documentation

### fetch_github

- **Purpose:** 
  - Fetches data from a specific GitHub repository endpoint.
- **Parameters:**
  - `owner` (str): The username or organization name owning the repository.
  - `repo` (str): The name of the repository.
  - `endpoint` (str): The specific API endpoint (e.g., "readme") to fetch data from.
- **Returns:**
  - JSON (dict): Returns the parsed JSON data if the request is successful.
  - `None`: If the request fails.

### fetch_github_repositories

- **Purpose:** 
  - Searches for GitHub repositories based on a query and returns a list of repositories.
- **Parameters:**
  - `query` (str): The search query string for repositories.
  - `max_results` (int, default=7): Maximum number of repositories to return.
- **Returns:**
  - List of dictionaries: Each dictionary contains repository information extracted from the GitHub search response.
  - Empty list: If the search fails.

### fetch_readme

- **Purpose:** 
  - Retrieves and decodes the README file for a given repository.
- **Parameters:**
  - `owner` (str): The username or organization name owning the repository.
  - `repo` (str): The name of the repository.
- **Returns:**
  - String: The decoded content of the README file.
  - Empty string: If no README is found or if an error occurs.

### analyze_repositories

- **Purpose:** 
  - Searches for repositories matching a query and filters them based on whether their README contains a specific context.
- **Parameters:**
  - `query` (str): The search keywords for repositories.
  - `context` (str): A string that must appear in the repository's README.
  - `max_results` (int, default=7): Maximum number of repositories to consider.
- **Returns:**
  - List of dictionaries: Each dictionary includes matched repository details such as name, owner, URL, description, and a snippet of the README.

### display_matched_repositories

- **Purpose:** 
  - Displays the list of repositories that matched the context in an organized format.
- **Parameters:**
  - `matched_repos` (list): A list of dictionaries holding the repository information.
- **Returns:**
  - None: The function prints the repository details to the console.

---

## Code Walkthrough

1. **Environment Setup:**
   - The script starts by importing necessary modules (`os`, `requests`, `dotenv`, and `langchain_core.documents`).
   - Environment variables are loaded using `load_dotenv()`, making the GitHub token available.

2. **GitHub Token:**
   - Retrieves the `GITHUB_TOKEN` from environment variables to authorize API requests.

3. **Function: fetch_github**
   - Constructs the URL for a given repository endpoint.
   - Sends an HTTP GET request with the Authorization header.
   - Returns JSON data if the response is successful or prints an error message if not.

4. **Function: fetch_github_repositories**
   - Constructs the URL for GitHub repository search.
   - Sends an HTTP GET request with the search query and maximum results.
   - Parses and returns the list of repositories, or an empty list if the request fails.

5. **Function: fetch_readme**
   - Calls `fetch_github` to retrieve the README data.
   - Uses the `base64` module to decode the content of the README.
   - Returns the decoded README content or an empty string if not available.

6. **Function: analyze_repositories**
   - Fetches repositories based on the provided search query.
   - For each repository, it fetches the README content.
   - Checks if the provided context exists within the README (case-insensitive) and collects matching repositories.
   - Each match includes repository details and a snippet (first 500 characters) of the README.

7. **Function: display_matched_repositories**
   - Takes the matched repository list and prints formatted details.
   - If no repositories match, it prints an appropriate message.

8. **Main Execution Block:**
   - Prompts the user for a search query and context string.
   - Calls `analyze_repositories` to filter the repositories.
   - Displays the filtered repositories using `display_matched_repositories`.

---

## Example Output

When running the script, a sample interaction might look like this:

```
Enter keywords to search repositories: data science
Enter the context to match in README files: visualization

Matched Repositories:
1. repo_name_1 (owner1)
   URL: https://github.com/owner1/repo_name_1
   Description: Repository description or "No description" if missing.
   README Snippet: <First 500 characters of the README content>
---
2. repo_name_2 (owner2)
   URL: https://github.com/owner2/repo_name_2
   Description: Repository description or "No description" if missing.
   README Snippet: <First 500 characters of the README content>
---
```

If no repositories are found, the script prints:

```
No repositories matched the given context.
```

---

## Error Handling

- **HTTP Status Checks:**  
  Each function making a request (`fetch_github` and `fetch_github_repositories`) checks the HTTP status code. If the status code is not 200, it prints an error message indicating the failure and returns `None` or an empty list.
  
- **Missing README Content:**  
  The `fetch_readme` function checks if the README data exists and contains the "content" key. If not, it prints a message indicating no README was found and returns an empty string.

- **User Interaction:**  
  The main block handles user inputs and provides output based on whether repositories match the provided context.

---

This comprehensive documentation should serve as a guide to understanding, installing, and using the GitHub Repository Analyzer script. Happy coding!