# Python Script Documentation

## Title
Document Querying with PDF Input using Streamlit and LLMs

## Overview
This script is a Streamlit application that allows users to upload PDF documents, processes them, and enables querying their content using a Large Language Model (LLM). The application handles file uploads, creates a vector index from the contents of the PDF, and allows users to input queries to receive answers based on the document contents.

## Installation & Dependencies
To run this script, you will need the following dependencies:
- `streamlit`: For creating the web application UI.
- `ipython`: For displaying formatted markdown.
- `llama_index`: A library required to handle LLM operations, querying, and embeddings.
- `uuid`: For generating unique identifiers for sessions.
- Ensure that the underlying LLM, in this case, the Ollama model and necessary embedding models from Hugging Face, are accessible.

You can install the required libraries using pip:
```bash
pip install streamlit ipython llama-index
```

## Usage
1. Run this script using Streamlit:
   ```bash
   streamlit run <script_name>.py
   ```
2. Open the web address provided by Streamlit in your browser.
3. Upload a PDF file using the file uploader in the sidebar.
4. Enter a query about the content of the uploaded PDF in the provided input box.

## Function/Class Documentation

### Function: `load_llm`
- **Purpose**: Load the LLM model for querying.
- **Input Parameters**: None.
- **Return Values**: 
  - Returns an instance of the `Ollama` model.

### Function: `reset_chat`
- **Purpose**: Resets the chat state by clearing messages and context.
- **Input Parameters**: None.
- **Return Values**: None.

### Function: `display_pdf`
- **Purpose**: Displays the uploaded PDF as an iframe in the Streamlit app.
- **Input Parameters**: 
  - `file` (File): The file-like object of the uploaded PDF.
- **Return Values**: None.

## Code Walkthrough
1. **Imports**: Essential libraries are imported, including Streamlit for UI and llama_index for LLM functionality.

2. **Session State Management**: 
   - A unique session ID is created using `uuid`, and a cache for uploaded files is initialized.

3. **Load LLM**:
   - The `load_llm` function is decorated with `@st.cache_resource` to cache the loaded LLM model for performance.

4. **Resetting Chat**:
   - The `reset_chat` function clears stored messages and context while performing garbage collection.

5. **Uploading Files**:
   - A file uploader widget allows users to upload PDF files. The uploaded file is saved to a temporary directory.

6. **PDF Processing**:
   - If successfully uploaded, the file is processed:
     - It checks if the file is already cached; if not, it loads the document using `SimpleDirectoryReader` and creates a vector index for querying.
     - Loads the LLM and embedding model.
     - Constructs a query engine for answering user queries.

7. **User Query Input**:
   - Users can input a query related to the uploaded document, and the application processes the query using the created query engine.

8. **Response Handling**:
   - The application checks if the response from the query is a generator and retrieves the final answer to display.

## Example Output
- If the PDF document contains information about "Machine Learning", and a user queries, "What is machine learning?", the app might respond with:
```
"Machine learning is a subset of artificial intelligence..."
```

## Error Handling
The script implements error handling using a try-except block during the file upload and processing. If any error occurs, an error message is displayed to the user in the Streamlit app indicating that something went wrong:
```python
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
```
This ensures that users receive feedback without crashing the app, maintaining a smoother experience.