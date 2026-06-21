import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer_stream(query, context_chunks):
        # join the chunks into one string to provide context
        context_text = "\n\n".join(context_chunks)
        
        # The system prompt tells the AI how to behave
        system_prompt = (
            "You are a helpful assistant. Use the provided context to answer the question. "
            "If the answer is not in the context, say you don't know. Keep it professional. "
        )
        
        # The user prompt contains the context and the actual question
        user_prompt = f"Context: \n{context_text} \n\nQuestion: {query}"
        
        # using stream = True to get a generator
        stream = client.chat.completions.create(
            model = 'llama-3.3-70b-versatile',
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            stream=True
        )
        
        return stream