# GitHub Repository Analyzer & RAG Updater

This script searches GitHub repositories using provided keywords, analyzes their README files for semantic similarity with a user-defined context, and integrates the matched repositories into a retrieval-augmented generation (RAG) system. In addition, it offers interactive Q&A capabilities using an agent and can generate a detailed README.md file for a selected repository.

---

## Overview

- **GitHub Search & Analysis:**  
  The script uses the GitHub API to search for repositories based on a user’s query and retrieves README contents.

- **Semantic Similarity:**  
  It leverages a Sentence Transformer model to embed README content and compare it against a user-provided context. Only repositories with a similarity above a threshold (0.75) are selected.

- **Parallel Processing:**  
  To improve performance, repository analysis is executed concurrently using a thread pool.

- **RAG Integration:**  
  The selected repository README snippets are added to an AstraDB-backed vector store, which is then hooked into a retriever tool for question answering using OpenAI's language model.

- **Interactive Agent:**  
  It creates a tool-calling agent that enables users to ask questions about the repositories and receive appropriate answers.

- **README Generation:**  
  The script can auto-generate a detailed README.md file for the top matched repository based on a preset template.

---

## Installation & Dependencies

### Dependencies

- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [langchain](https://github.com/hwchase17/langchain)
- [sentence-transformers](https://pypi.org/project/sentence-transformers/)
- [langchain_astradb](https://github.com/hwchase17/langchain_astradb) (or similar AstraDB integration)
- [langchain_openai](https://github.com/hwchase17/langchain_openai)

### Installation

Use pip to install the necessary dependencies:

```bash
pip install requests python-dotenv langchain sentence-transformers langchain_astradb langchain_openai
```

Additionally, ensure you have a `.env` file in your project directory with the following tokens and API endpoints:
- `GITHUB_TOKEN`
- `ASTRA_DB_API_ENDPOINT`
- `ASTRA_DB_APPLICATION_TOKEN`
- `ASTRA_DB_KEYSPACE` (optional)

---

## Usage

1. **Run the Script:**

   Execute the script directly:
   ```bash
   python script_name.py
   ```

2. **Input Prompts:**

   - The script prompts you for a search query (keywords for searching repositories).
   - You will later be asked for context to compare against README contents.
   - An interactive session will begin for any questions regarding matched repositories.
   - Finally, you can opt to generate a README.md file for the top matched repository.

3. **Example:**

   ```
   Enter keywords to search repositories: machine learning
   Enter the context to match in README files: project utilizing deep learning for image recognition
   Matched Repositories:
   1. repoName (ownerName)
      URL: https://github.com/ownerName/repoName
      Description: A repository for deep learning projects.
      Similarity: 0.82
      README Snippet: # Project Title... (first 500 characters)
   ---
   Do you want to update the RAG with matched repositories? (y/N): y
   Ask a question about matched repositories (q to quit): What is the main functionality?
   [Agent Output]
   Ask a question about matched repositories (q to quit): q
   Do you want to generate a README.md file for the top matched repository? (y/N): y
   README.md file generated and saved as repoName_README.md.
   ```

---

## Function/Class Documentation

### fetch_github(owner, repo, endpoint)
- **Purpose:**  
  Fetches a JSON response from a specified GitHub repository endpoint.
- **Parameters:**
  - `owner` (str): Repository owner’s username.
  - `repo` (str): Repository name.
  - `endpoint` (str): Specific repository endpoint to query (e.g., 'readme').
- **Returns:**  
  - `dict` containing the fetched data if successful.
  - `None` if the API request fails.

### fetch_github_repositories(query, max_results=7)
- **Purpose:**  
  Searches GitHub repositories based on a query string and returns a list of repository items.
- **Parameters:**
  - `query` (str): Search query for repositories.
  - `max_results` (int, optional): Maximum number of repositories to retrieve (default is 7).
- **Returns:**  
  - `list` of repository items (dictionaries) on success.
  - An empty list if the API request fails.

### fetch_readme(owner, repo)
- **Purpose:**  
  Retrieves and decodes the README content for a given repository.
- **Parameters:**
  - `owner` (str): Repository owner’s username.
  - `repo` (str): Repository name.
- **Returns:**  
  - `str` containing the decoded README content if available.
  - An empty string if no README is found.

### analyze_repository(repo, context_embedding)
- **Purpose:**  
  Compares a repository’s README with a context embedding to determine if it semantically matches.
- **Parameters:**
  - `repo` (dict): Repository information as returned by the GitHub API.
  - `context_embedding` (tensor): Precomputed embedding for the user’s context.
- **Returns:**  
  - `dict` with repository details and similarity score if similarity exceeds threshold (0.75).
  - `None` if the repository does not match the context.

### analyze_repositories(query, context, max_results=7)
- **Purpose:**  
  Searches and analyzes all repositories based on the provided query and context.
- **Parameters:**
  - `query` (str): GitHub search query.
  - `context` (str): Text context to compare against README contents.
  - `max_results` (int, optional): Maximum number of repositories to analyze.
- **Returns:**  
  - `list` of dictionaries containing matched repository details, sorted by similarity.

### display_matched_repositories(matched_repos)
- **Purpose:**  
  Displays the list of repositories that matched the given context.
- **Parameters:**
  - `matched_repos` (list): List of dictionaries with repository details.
- **Returns:**  
  - None (prints output directly to the console).

### connect_to_vstore()
- **Purpose:**  
  Establishes a connection to an AstraDB-backed vector store for document storage and retrieval.
- **Parameters:**  
  - None.
- **Returns:**  
  - An instance of AstraDBVectorStore configured with the provided credentials and namespace.

### generate_readme(repository, context)
- **Purpose:**  
  Generates a detailed README.md file for a given repository using predefined sections.
- **Parameters:**
  - `repository` (dict): Contains repository details such as name, owner, URL, and description.
  - `context` (str): Context information, available for potential further customization (not directly used in the template).
- **Returns:**  
  - None (creates a README.md file on the disk and prints a confirmation).

---

## Code Walkthrough

1. **Environment Setup:**  
   - The script begins by importing required modules.
   - Environment variables are loaded using the `dotenv` package to access tokens and API endpoints.

2. **API Functions:**  
   - The functions `fetch_github`, `fetch_github_repositories`, and `fetch_readme` handle interactions with the GitHub API.
   - These functions include error messages printed to the console when an API call fails.

3. **Semantic Analysis:**
   - A Sentence Transformer model (`all-MiniLM-L6-v2`) is initialized to convert README texts and context into embeddings.
   - `analyze_repository` computes the cosine similarity between README embeddings and the provided context.
   - `analyze_repositories` processes the repository list concurrently with `ThreadPoolExecutor` to speed up computation.

4. **Results Display:**  
   - `display_matched_repositories` function prints matched repositories, showing the repository name, URL, description, similarity score, and a snippet of the README.

5. **Vector Store Integration:**  
   - `connect_to_vstore` connects to an AstraDB vector store using OpenAI embeddings.
   - Matched repository README snippets are converted into Document objects and added to the vector store after attempting deletion of any earlier collection data.

6. **Agent Setup & Q&A Loop:**  
   - A retriever tool is created based on the vector store.
   - An interactive agent is assembled using an OpenAI chat model and retriever tool.
   - The script then enters a loop where users can ask questions about the repositories until they decide to quit.

7. **README Generation:**  
   - Optionally, the user can choose to generate a comprehensive README.md file for the top matched repository using the `generate_readme` function.

---

## Example Output

After executing the script, a typical console interaction might look like:

```
Enter keywords to search repositories: machine learning
Enter the context to match in README files: deep learning for image recognition

Matched Repositories:
1. repoName (ownerName)
   URL: https://github.com/ownerName/repoName
   Description: Implementation of deep learning models.
   Similarity: 0.82
   README Snippet: # Repository Title ... [first 500 characters]
---

Do you want to update the RAG with matched repositories? (y/N): y
Ask a question about matched repositories (q to quit): What libraries are used?
[Agent Output]: The repository uses Python along with TensorFlow and PyTorch...
Ask a question about matched repositories (q to quit): q
Do you want to generate a README.md file for the top matched repository? (y/N): y
README.md file generated and saved as repoName_README.md.
```

---

## Error Handling

- **API Request Failures:**  
  Each function that interacts with the GitHub API (`fetch_github`, `fetch_github_repositories`, `fetch_readme`) checks the HTTP status code. If it is not 200, an error message is printed and the function returns a fallback value (`None` or an empty collection).

- **Missing README Content:**  
  `fetch_readme` function checks for the existence of the "content" key in the response. If missing, it logs an error message indicating that no README was found.

- **Vector Store Deletion:**  
  In the RAG update section, a try-except block is used to attempt deletion of the current vector store collection. Any exceptions during deletion are silently passed, allowing the script to continue execution.

- **General Input Validation:**  
  The script uses simple conditional checks (e.g., comparing user input to "q") to manage the interactive session gracefully.

---

This detailed documentation provides an overview and in-depth analysis of the script, including its core functions, usage instructions, and key error handling mechanisms.