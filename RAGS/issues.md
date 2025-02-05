# GitHub Issues and Repositories Search & Update Tool

This script is designed to interact with GitHub repositories and issues while leveraging a vector store powered by AstraDB and the LangChain framework. It provides a command-line interface (CLI) where users can either search for repositories based on keywords or ask questions about GitHub issues, with an underlying agent handling information retrieval and intelligent responses.

---

## Overview

- Connects to an AstraDB-backed vector store using embeddings from OpenAI.
- Enables updating the vector store with GitHub issues for a selected repository.
- Integrates a retrieval tool with LangChain to answer questions about GitHub issues.
- Supports searching for GitHub repositories using keywords, updating the issue database accordingly.
- Implements an interactive command-line loop where users can choose between:
  - Searching for repositories (option "r").
  - Asking questions about stored GitHub issues (option "i").
  - Quitting the script (option "q").

---

## Installation & Dependencies

### Dependencies

Ensure that the following Python packages are installed:

- python-dotenv  
- requests  
- langchain_openai  
- langchain_astradb  
- langchain  
- langchain.agents  
- langchain.tools  
- langchain.hub  
- A custom GitHub module that provides:  
  - fetch_github_issues  
  - fetch_github_repositories  
  - load_issues (if needed)  

### Installation

Use pip to install any third-party packages. For example:

```bash
pip install python-dotenv requests langchain_openai langchain_astradb
```

If the custom GitHub module is not available on PyPI, ensure that it is included in your project or installed from its source repository.

Ensure that you have a valid .env file configured with the following variables:

- ASTRA_DB_API_ENDPOINT  
- ASTRA_DB_APPLICATION_TOKEN  
- ASTRA_DB_KEYSPACE  

---

## Usage

Run the script from the command line:

```bash
python your_script.py
```

### Interaction Examples

1. **Repository Search**
   - The script will ask:  
     "Do you want to search for repositories (r) or ask about issues (i)? (q to quit):"
   - If you press `r`, you will be prompted to enter keywords.
   - The script fetches and displays the top 5 matching repositories.
   - Choose a repository by entering its corresponding number.
   - The script updates the issue vector store with issues from the selected repository.

2. **Issues Query**
   - By choosing `i`, you can type a question regarding GitHub issues.
   - The agent processes the query using the embedded retriever tool.
   - The response is then displayed on the console.

3. **Quit**
   - Type `q` during a prompt to exit the script.

---

## Function/Class Documentation

### connect_to_vstore()
- **Purpose:**  
  Connects to the AstraDB vector store using OpenAI embeddings and environment variables.
  
- **Parameters:**  
  None
  
- **Returns:**  
  - vstore (AstraDBVectorStore): A vector store instance that is used for storing and retrieving documents (issues).

- **Usage Example:**
  ```python
  vstore = connect_to_vstore()
  ```

---

### update_issues(owner, repo)
- **Purpose:**  
  Fetches GitHub issues for a given repository and updates the AstraDB vector store.

- **Parameters:**  
  - owner (str): The GitHub username or organization name owning the repository.
  - repo (str): The name of the repository.

- **Returns:**  
  None  
  (The function updates the global vector store `vstore` with fetched issues data.)

- **Usage Example:**
  ```python
  update_issues("google", "it-cert-automation-practice")
  ```

---

## Code Walkthrough

1. **Environment Setup:**
   - The script begins by importing necessary modules and loading environment variables using `load_dotenv()`.
   - Environment variables provide access credentials and endpoints for the AstraDB service.

2. **Vector Store Connection:**
   - The `connect_to_vstore()` function is defined and called to instantiate a vector store (`vstore`) using OpenAI embeddings.
   - The function checks for a specified namespace via the environment variable and configures the vector store accordingly.

3. **Issue Updates:**
   - The `update_issues(owner, repo)` function fetches issues from GitHub for a given repository using `fetch_github_issues()`.
   - It attempts to delete the old collection using `vstore.delete_collection()`. An exception is caught to avoid crashing if deletion fails.
   - A fresh connection to the vector store is made, and the fetched issues are added using `vstore.add_documents(issues)`.

4. **Retriever and Agent Setup:**
   - A retriever is created from the vector store with a search keyword parameter (`k=3`) to return the top three similar documents.
   - The retriever tool is created using `create_retriever_tool()`, which links the retriever to the tool name "github_search".
   - A prompt is loaded using `hub.pull()` to initialize an agent with the LangChain framework.  
   - A language model instance (`ChatOpenAI()`) is set up for processing natural language queries.
   - An agent is created with the tools list (currently including just the retriever tool) using `create_tool_calling_agent()`.
   - An `AgentExecutor` is created to manage the tool interactions.

5. **Interactive Loop:**
   - The script enters an infinite loop where the user chooses an action:
     - **Action "r"** (repository search):
       - Prompts for keywords to search for repositories using `fetch_github_repositories()`.
       - Displays the top five matches and asks the user to select one.
       - Updates the issues in the vector store for the selected repository by calling `update_issues()`.
     - **Action "i"** (issue query):
       - The user submits a question related to GitHub issues.
       - The question is processed by the agent executor, and the result is printed.
     - **Action "q"**:  
       - Exits the loop and ends the script.
     - For any invalid input, the script provides an "Invalid action" message.

---

## Example Output

Upon running the script, a typical console session might look like:

```
Do you want to search for repositories (r) or ask about issues (i)? (q to quit): r
Enter keywords to search GitHub repositories: automation testing
Top 5 repositories matching your query:
1. org/repository-one
2. org/repository-two
3. org/repository-three
4. org/repository-four
5. org/repository-five
Select a repository (1-5): 2
Issues updated for repository org/repository-two

Do you want to search for repositories (r) or ask about issues (i)? (q to quit): i
Ask a question about github issues (q to quit): How are issues prioritized?
[Agent Output]: Based on the similarity search, the issues indicate that priority is determined by user feedback and bug severity...
```

---

## Error Handling

- **Vector Store Deletion:**  
  Inside `update_issues()`, the script attempts to delete the current vector store collection. A bare exception handler (`except:`) is used to prevent the script from crashing in case the deletion fails (e.g., if the collection does not exist).

- **User Input Validation:**  
  When selecting a repository from the search results, the script checks if the entered index is within the valid range. If not, it informs the user with "Invalid selection".

- **Input Loop Exit:**  
  The interactive loop monitors for the input of `"q"` to properly exit the program.

---

This detailed documentation should help understand and maintain the Python script, while also providing guidance for future extensions or troubleshooting. Enjoy using the tool to explore and interact with GitHub data!