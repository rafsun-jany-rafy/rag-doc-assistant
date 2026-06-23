import streamlit as st
import requests

st.set_page_config(page_title="Cloud Doc Assistant", page_icon="📄")
st.title("📄 Cloud-Powered Document Assistant ")

# backend URL
# API_URL = "http://localhost:8000"
BASE_URL = "http://127.0.0.1:8000"

# sidebar file upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file and st.button("Index Doxument"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        st.success(response.json()["message"])

# initialize and display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# chat interface
if prompt := st.chat_input("Ask a question"):
    # show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # get assistant response  
    with st.chat_message("assistant"):
        # calling FastAPI endpoint
        response = requests.post(f"{BASE_URL}/ask", data={"query": prompt}, stream=True)
        
        if response.status_code == 200:
            # stream the response from FastAPI to streamlit
            # st.write to handle the text flow
            def stream_gen():
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    yield chunk
                    
            full_response = st.write_stream(stream_gen())
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        else:
            st.error("Backend error.")