import streamlit as st
import requests
import os
import json

# config and assets
st.set_page_config(page_title="Cloud Doc Assistant", page_icon="📄", layout="wide")
st.title("📄 Cloud-Powered Document Assistant ")

# backend URL
# API_URL = "http://localhost:8000"
# BASE_URL = "http://127.0.0.1:8000"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
HISTORY_FILE = "chat_history.json"

# custom CSS
st.markdown("""
    <style>
    /* Move the whole app content higher */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    /* The Parallel Header Container */
    .header-wrapper {
        display: flex;
        align-items: center; /* Vertically centers the logo and text */
        justify-content: flex-start;
        margin-bottom: -10px; /* Tightens space before the divider */
    }

    .logo-text-container {
        margin-left: 20px; /* Space between logo and text */
    }

    .chat-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#ff4b4b, #ff8a8a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }

    .tagline {
        font-style: italic;
        color: #888;
        margin: 0;
        font-size: 1.1rem;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #666666;
        text-align: center;
        padding: 5px 0px;
        font-size: 0.75rem;
        z-index: 1000;
    }
    .stChatInput {
        margin-bottom: 20px;
    }              
    </style>
    """, unsafe_allow_html=True)

# persistence logic
def save_history(messages):
    with open(HISTORY_FILE,"w") as f:
        json.dump(messages, f)
        
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


# app layout
# sidebar file upload
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    
    if st.button("🗑️ Reset All Data"):
        requests.post(f"{BACKEND_URL}/clear")
        if os.path.exists(HISTORY_FILE): 
            os.remove(HISTORY_FILE)
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    # st.markdown("### Upload Knowledge")
    uploaded_file = st.file_uploader("### Upload PDF", type="pdf")
    
    if uploaded_file and st.button("⚡ Index Doxument"):
        with st.spinner("Analyzing PDF..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
            st.success(response.json()["message"])
    

# HEADER SECTION 
st.markdown("""
    <div class="header-wrapper">
        <div style="font-size: 75px; line-height: 1;">🧠</div>
        <div class="logo-text-container">
            <p class="chat-header">DocuMind AI</p>
            <p class="tagline">Intelligent Retrieval-Augmented Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---") # The horizontal divider

# chat theme
# initialize and display chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# chat interfece and user input
if prompt := st.chat_input("Ask a question"):
    # show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(st.session_state.messages) # save immediately
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # get assistant response  
    with st.chat_message("assistant"):
        # calling FastAPI endpoint
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/ask", data={"query": prompt}, stream=True)
        
        if response.status_code == 200:
            # stream the response from FastAPI to streamlit
            # st.write to handle the text flow
            def stream_gen():
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    yield chunk
                    
            full_response = st.write_stream(stream_gen())
            
            # save assistant reply
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_history(st.session_state.messages)
            
        else:
            st.error("Error connecting to AI server.")
            
# footer
st.markdown("""
            <div class="footer">
                <p> Built with using FastAPI + Groq + Llama 3.2</p>
            </div>
            """, unsafe_allow_html=True)