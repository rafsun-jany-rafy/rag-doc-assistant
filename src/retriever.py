import faiss
import numpy as np
import os
import pickle

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "..","vectorstore")

def create_vector_store(chunks, embeddings):
    
    # 1. Convert embeddings to a numpy array (FAISS requirements)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    # 2. Save the FAISS index
    faiss.write_index(index, os.path.join(VECTOR_STORE_PATH, "index.faiss"))
    
    # 3. Save the actual text chunks so that we can read them later
    with open(os.path.join(VECTOR_STORE_PATH, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
        
    print("Vector store created and saved to /vectorstore")
    
def retrieve_docs(query_embedding, top_k =3):
    # 1. Load the index
    index = faiss.read_index(os.path.join(VECTOR_STORE_PATH, "index.faiss"))
    
    # 2. Load the chunks
    with open(os.path.join(VECTOR_STORE_PATH, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)
        
    # 3. Search the index
    # query_embedding needs to be a 2D array
    distances, indices = index.search(np.array([query_embedding]), top_k)
    
    # 4. Return the matching text chunks
    results = [chunks[i] for i in indices[0]]
    return results