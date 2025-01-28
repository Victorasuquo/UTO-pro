import os
import streamlit as st
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key, model_name="text-embedding-3-small"
)

# Initialize the Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name, embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

# Function to split text into chunks
def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# Function to generate embeddings using OpenAI API
def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embedding = response.data[0].embedding
    return embedding

# Function to query documents
def query_documents(question, n_results=2):
    results = collection.query(query_texts=question, n_results=n_results)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    return relevant_chunks

# Function to generate a response from OpenAI
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    
    # Modify prompt to enforce structured, clean format
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. Format your answer with clean headings, bullet points, and line breaks. "
        "For example: Provide a 'Purpose' section, a 'Primary Functionality' section with bullet points, etc."
        "If you don't know the answer, say that you don't know. Keep the response concise and well-structured."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )

    # Return the message content from the response
    return response.choices[0].message.content

# Streamlit UI
st.title("UTOM: Intelligent Document Query System")

# File uploader for Markdown files
uploaded_files = st.file_uploader(
    "Upload markdown files (.md):", type=["md"], accept_multiple_files=True
)

# Process uploaded files
documents = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        text = uploaded_file.read().decode("utf-8")
        documents.append({"id": uploaded_file.name, "text": text})

    st.write(f"Loaded {len(documents)} documents.")

    # Split and process documents
    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})

    # Generate embeddings and upsert into Chroma
    for doc in chunked_documents:
        doc["embedding"] = get_openai_embedding(doc["text"])
        collection.upsert(
            ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]
        )
    st.success("Documents processed and stored in Chroma!")

# Query input
question = st.text_input("Ask a question:")
if question:
    relevant_chunks = query_documents(question)
    if relevant_chunks:
        answer = generate_response(question, relevant_chunks)
        
        # Display the answer using markdown for better readability
        st.markdown(f"### Answer:\n{answer}")
    else:
        st.write("No relevant documents found.")
