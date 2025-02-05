# Streamlit PDF Document Query Interface Documentation

This document provides an in-depth explanation of a Python script that leverages Streamlit for a web interface, integrates LlamaIndex for processing PDF documents, and utilizes an LLM (via Ollama) along with a HuggingFace embedding model to answer natural language queries about the contents of the uploaded PDF.

---

## Overview

The script creates an interactive Streamlit application that allows users to upload PDF documents through a sidebar. Upon file upload, the script:

- Temporarily saves the PDF file.
- Reads the document using a directory reader.
- Indexes the document with a vector store utilizing embeddings from HuggingFace.
- Sets up an LLM via Ollama to answer queries based on the document’s content.
- Provides a text input field for users to ask questions about the document.
- Displays the LLM-generated answer in real time.

It also caches the query engine per uploaded file for improved performance and efficiency.

---

## Installation & Dependencies

### Dependencies

The script requires the following Python packages:

- Python standard libraries: `os`, `base64`, `gc`, `tempfile`, `time`, `uuid`
- Third-party libraries:
  - [Streamlit](https://streamlit.io/) – for building web applications.
  - [IPython](https://ipython.org/) – for displaying rich content (used here for Markdown rendering).
  - [llama_index](https://github.com/jerryjliu/llama_index) – for document indexing and query engine creation.
  - [Ollama](https://ollama.com/) – LLM interface (accessed through the llama_index package).
  - [HuggingFaceEmbedding](https://huggingface.co/) – for generating embeddings using a specific model.

### Installation Steps

1. Ensure Python 3.7 or higher is installed.
2. Install the required packages using pip. For example:
   ```
   pip install streamlit ipython
   pip install llama-index
   pip install <any additional packages or requirements for Ollama and HuggingFaceEmbedding>
   ```
3. Confirm that the HuggingFace model "BAAI/bge-large-en-v1.5" and the Ollama model "deepseek-r1:1.5b" are available and accessible.

---

## Usage

### Running the Script

1. Save the script to a Python file, for example, `pdf_query_app.py`.
2. Run the Streamlit app from the command line:
   ```
   streamlit run pdf_query_app.py
   ```
3. The app will open in the browser. Use the sidebar to:
   - Upload a `.pdf` file.
   - Once indexed, enter your query about the document in the provided text input.
4. The application will process your query, and the LLM-generated answer will be displayed below the query input.

---

## Function & Class Documentation

### load_llm

- **Purpose:**  
  Initializes and caches an instance of the Ollama LLM model.
  
- **Parameters:**  
  None.
  
- **Returns:**  
  - *llm (Ollama)*: An instance of the Ollama model configured with `model="deepseek-r1:1.5b"` and a request timeout value.

- **Implementation Details:**
  The function is decorated with `@st.cache_resource` so that the LLM is loaded once and reused across interactions.

---

### reset_chat

- **Purpose:**  
  Resets the conversation context by clearing session messages and context, and triggers garbage collection.

- **Parameters:**  
  None.
  
- **Returns:**  
  None.
  
- **Implementation Details:**
  This function clears the `st.session_state.messages` and `st.session_state.context` and calls `gc.collect()` to free up resources.

---

### display_pdf

- **Purpose:**  
  Provides a preview of the uploaded PDF by converting its binary data to a base64 string and rendering it in an iframe.
  
- **Parameters:**
  - `file` (*file-like object*): The file object representing the PDF uploaded by the user.
  
- **Returns:**  
  None (displays the PDF inline via Streamlit's markdown rendering).

- **Implementation Details:**
  Uses base64 encoding to display the PDF within an HTML `<iframe>` using Streamlit’s `st.markdown`.

---

## Code Walkthrough

1. **Imports and Session Initialization:**
   - The script starts by importing necessary libraries and modules.
   - A unique session identifier (`st.session_state.id`) is generated if it is not already present. This allows associating cached query engines with a user session.
   - A global variable `client` is defined (but not used further in this snippet).

2. **LLM Loading and Caching:**
   - The `load_llm()` function is defined and decorated with `@st.cache_resource` to ensure that the LLM instance (Ollama model) is loaded only once per session.

3. **Chat Context Reset Function:**
   - The `reset_chat()` function is implemented to clear the chat history in the session state.

4. **PDF Display Function:**
   - The `display_pdf(file)` function is provided to generate and render a PDF preview.

5. **Streamlit Sidebar for Document Upload:**
   - The sidebar prompts the user to upload a `.pdf` file.
   - Once a file is uploaded, the script saves the file temporarily using Python's `tempfile.TemporaryDirectory()`.
   - A unique key is created to check if the document has already been cached in `st.session_state.file_cache`.

6. **Document Indexing:**
   - If the file has not been previously processed, the script uses `SimpleDirectoryReader` to load the PDF content.
   - The LLM and embedding model are initialized:
     - `load_llm()` is called to get the LLM instance.
     - A HuggingFace embedding model is instantiated for vector embeddings.
   - The settings for the embedding and LLM models are updated in the `Settings` object from `llama_index`.
   - A `VectorStoreIndex` is created from the loaded documents with progress feedback.
   - A query engine is created from the vector store index, configured for streaming responses.
   - A custom prompt template (`qa_prompt_tmpl`) is defined to guide the LLM on how to answer queries based on the provided context.
   - The prompt template is updated in the query engine.
   - The query engine is stored in the session-state cache using the unique file key.

7. **Query Input and Processing:**
   - The main area of the app provides a text input for users to enter their queries.
   - Upon entering a query, the script invokes the query engine.
   - The script checks if the response is a generator (streaming response) and concatenates the tokens, or notifies if no response is generated.
   - The final answer is then displayed on the page.

8. **Error Handling:**
   - The entire document processing and querying logic are enclosed within a try-except block.
   - Any exceptions encountered during processing result in an error message displayed via `st.error`.

---

## Example Output

- **Upon Document Upload:**
  - The sidebar displays "Indexing your document..." while processing.
  
- **After Entering a Query:**
  - The main area of the app displays the LLM’s generated answer which could be a detailed explanation based on the document’s content.
  
- **PDF Preview (if used):**
  - An embedded PDF preview is shown in an iframe, allowing users to verify the uploaded content.

---

## Error Handling

- **File Processing:**
  - If the temporary directory or the file is not found, the user is informed with an appropriate error message.
  
- **General Exception Catch:**
  - The entire process is wrapped in a try-except block to catch any unexpected errors.
  - An error message is rendered in the UI using `st.error` if an exception occurs.

---

This documentation provides a detailed insight into each component of the script, explaining its purpose, implementation, and how the overall application functions. Use this guide as a reference to understand, maintain, or extend the functionality of the script.