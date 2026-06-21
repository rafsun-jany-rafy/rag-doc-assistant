# from openai import OpenAI 
# import os
# from dotenv import load_dotenv

# load_dotenv()


# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def get_embedding(text):
#     response = client.embeddings.create(
#         model = "text-embedding-3-small",
#         input=text
#     )
    
#     return response.data[0].embedding

from sentence_transformers import SentenceTransformer
import numpy as np

# This model is small (about 80MB) and will download automatically the first time
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    """
    Takes a list of text chunks and returns a list of numerical embeddings.
    """
    embeddings = model.encode(text, convert_to_numpy=True)
    return embeddings