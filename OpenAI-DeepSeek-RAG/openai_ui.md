```markdown
# Intelligent Document Query System (UTOM)

## Overview
The Intelligent Document Query System (UTOM) is a robust application built using Streamlit that allows users to upload Markdown documents, split them into smaller chunks, generate embeddings using OpenAI, and perform document queries. The system retrieves relevant chunks of information based on the user's query and generates structured responses.

## Installation & Dependencies
To run this script, ensure you have the following dependencies installed:

- `streamlit`
- `python-dotenv`
- `chromadb`
- `openai`

You can install these dependencies using pip:

```bash
pip install streamlit python-dotenv chromadb openai
```

You also need to set up an `.env` file in your project directory containing the following variable:

```
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage
To run the application, execute the following command in your terminal:

```bash
streamlit run your_script_name.py
```

This script provides a user interface to upload Markdown files and query them.

### Example Workflow

1. Upload Markdown files using the provided file uploader.
2. Enter a question in the text input box to query the documents.
3. View the generated answer displayed in a structured format.

## Function/Class Documentation

### `split_text(text, chunk_size=1000, chunk_overlap=20)`
- **Purpose**: Splits a given text into smaller chunks with defined size and overlap.
- **Input Parameters**:
  - `text` (str): The text to be split.
  - `chunk_size` (int, optional): The size of each text chunk. Default is 1000.
  - `chunk_overlap` (int, optional): The number of overlapping characters between chunks. Default is 20.
- **Return Values**:
  - (list of str): A list of text chunks.

### `get_openai_embedding(text)`
- **Purpose**: Generates an OpenAI embedding for the given text.
- **Input Parameters**:
  - `text` (str): The text for which to create an embedding.
- **Return Values**:
  - (list): The embedding vector for the input text.

### `query_documents(question, n_results=2)`
- **Purpose**: Queries the document collection to find relevant chunks based on the user's question.
- **Input Parameters**:
  - `question` (str): The user's question.
  - `n_results` (int, optional): The number of results to return. Default is 2.
- **Return Values**:
  - (list of str): A list of relevant document chunks.

### `generate_response(question, relevant_chunks)`
- **Purpose**: Generates a response from OpenAI based on the provided question and relevant chunks.
- **Input Parameters**:
  - `question` (str): The user's question.
  - `relevant_chunks` (list of str): The chunks of text relevant to the question.
- **Return Values**:
  - (str): Formatted response string from OpenAI.

## Code Walkthrough
1. **Environment Setup**: The script begins by loading environment variables and initializing the OpenAI and Chroma clients.
2. **Document Upload**: Through the Streamlit UI, users can upload Markdown files. Upon upload, the text is read and stored in a list.
3. **Text Chunking**: The script splits the texts into chunks and retains necessary overlaps to ensure smoother context retrieval.
4. **Embedding Generation**: Each chunk is converted into an embedding using the OpenAI API, which is then stored in the Chroma collection for querying.
5. **Query Processing**: Users can input their questions, which trigger searching through relevant document chunks.
6. **Response Generation**: A structured response is generated based on the context retrieved from the document chunks.

## Example Output
When a user uploads documents and asks a question, the system will output something like this:

```
### Answer:
**Purpose**: This system allows users to query documents intelligently.

**Primary Functionality**:
- Upload documents in Markdown format.
- Generate embeddings for efficient querying.
- Retrieve and display structured answers based on user queries.
```

## Error Handling
The script contains basic checks to ensure uploaded files are processed correctly and to handle cases where no relevant documents are found. Users receive clear messages indicating the processing status and any relevant errors during execution.
```