import os
from src.ingest import load_path, split_text
from src.embeddings import get_embedding
from src.retriever import create_vector_store, retrieve_docs

def ingest_document(pdf_path):
    """Call this only when a new PDF is uploaded."""
    # 1. Read and split the pdf
    text = load_path(pdf_path)
    chunks = split_text(text)
    
    # 2. Convert chunks into numbers(embedding)
    embeddings = get_embedding(chunks)
    
    # 3. Store into vector database
    create_vector_store(chunks, embeddings)
    
    return len(chunks)

def get_relevant_context(user_query):
    """Call this for every question."""
    # 4. Convert user's question into a vector
    query_vec = get_embedding([user_query])[0]
    
    # 5. Find top 5 most relevant chunks
    relevant_chunks = retrieve_docs(query_vec, top_k=5)
    
    return relevant_chunks


# from src.llm import generate_answer

# def run_rag_pipeline(pdf_path, user_query):
#     # 1. Read and split the pdf
#     text = load_path(pdf_path)
#     chunks = split_text(text)
    
#     # 2. Convert chunks into numbers(embedding)
#     embeddings = get_embedding(chunks)
    
#     # 3. Store into vector database
#     create_vector_store(chunks, embeddings)
    
#     # 4. Convert user's question into a vector
#     query_vec = get_embedding([user_query])[0]
    
#     # 5. Find top 3 most relevant chunks
#     relevant_chunks = retrieve_docs(query_vec, top_k=3)
    
#     # 6. Send those chunks and question to Llama 3.2
#     answer = generate_answer(user_query, relevant_chunks)
    
#     return answer