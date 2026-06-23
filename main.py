from fastapi import FastAPI, Form, UploadFile, File
from pydantic import BaseModel
from src.pipeline import ingest_document, get_relevant_context
from src.llm import generate_answer_stream
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

# folder to store uploads
UPLOAD_DIR = "data/documents"

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    num_chunks = ingest_document(file_path)
    return  {"message": f"File {file.filename} indexed.", "chunks": num_chunks}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    print(f"Question recieved: {query}")
    
    # 1. get context
    relevant_chunks = get_relevant_context(query)
    print(f" Found {len(relevant_chunks)} chunks of context.")
    
    # 2. return a stream of text
    def stream_response():
        try:
            stream = generate_answer_stream(query, relevant_chunks)
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    print(token, end=" ", flush=True)
                    yield token
        
        except Exception as e:
            ptint(f"Groq error: {e}")
            yield f"Error: {str(e)}"
        
                
    return StreamingResponse(stream_response(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host =  "127.0.0.1", port = 8000)