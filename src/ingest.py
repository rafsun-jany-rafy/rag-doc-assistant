import fitz

# Reading the pdf and extracting text
def load_path(file_path):
    
    document = fitz.open(file_path)
    
    text = ""
    
    for page in document:
        text += page.get_text()
        
    return text


# Splitting large texts into smaller chunks
def split_text(text, chunk_size=200, overlap=50):
    
    words = text.split()
    
    chunks = []
    
    # Slide the window by (chunk size - overlap)
    # for i in range(0, len(words), chunk_size):
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(
            words[i:i + chunk_size]
        )
        
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
        
    return chunks