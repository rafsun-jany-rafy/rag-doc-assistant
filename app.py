import streamlit as st
import os
from src.pipeline import ingest_document, get_relevant_context
from src.llm import generate_answer_stream

# page config
st.set_page_config(page_title="AI Doc Assistant", page_icon="📄")

st.title("📄 AI Document Assistant(Local Llama 3.2)")
st.markdown("---")

# 1. Sidebar for file upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        # Save the file to data/documents folder
        file_path = os.path.join("data", "documents", uploaded_file.name)
        
        # Only index if it's a new file
        if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
            with st.spinner("Indexing document..."):
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                num_chunks = ingest_document(file_path)
                st.session_state.current_file = uploaded_file.name
                st.success(f"Indexed {num_chunks} chunks!")
        
# 2. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

# 3. User input
if prompt := st.chat_input("Ask a question about the PDF..."):
    # Add user message to history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    if "current_file" in st.session_state:
        with st.chat_message("assistant"):
            # 1. Get context(fast)
            relevant_chunks = get_relevant_context(prompt)

            # 2. Stream the answer
            respone_placeholder = st.empty()
            full_response = ""
            
            # This logic create the typing effect
            stream = generate_answer_stream(prompt, relevant_chunks)
            
            # we use st.write_stream for easiest implementation
            full_response = st.write_stream(chunk['message']['content'] for chunk in stream)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    else:
        st.warning("Please upload a PDF first")
        
        
    # """# Check if a file was uploaded first
    # if uploaded_file:
    #     with st.chat_message("assistant"):
    #         with st.spinner("Analyzing document with Llama 3.2..."):
    #             # Call pipeline
    #             file_path = os.path.join("data", "documents", uploaded_file.name)
    #             response = run_rag_pipeline(file_path, prompt)
                
    #             st.markdown(response)
    #             # Add assistant response to history
    #             st.session_state.messages.append({"role": "assistant", "content": response})
    # else:
    #     st.warning("Please upload a PDF file first using the sidebar.")"""
       
   