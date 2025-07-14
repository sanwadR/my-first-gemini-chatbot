import streamlit as st
import os
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot")
st.caption("Powered by Google's Gemini (Free API)")

# Load the Gemini API key
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("❌ Gemini API key is missing. Please add it in .streamlit/secrets.toml or as an environment variable.")
    st.stop()

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# Initialize Gemini Model (this uses the correct API version!)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                reply = f"❌ Error: {str(e)}"
            st.markdown(reply)
            st.session_state.chat_history.append(("assistant", reply))
