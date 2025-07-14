import streamlit as st
import google.generativeai as genai
import datetime

gemini_api_key = st.secrets["GEMINI_API_KEY"]
# 🔑 Replace with your actual Gemini API key
genai.configure(api_key=gemini_api_key)

# 🌟 Set model ID for context-aware chat
MODEL_ID = "gemini-1.5-flash-latest"

# Initialize the chat session
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = genai.GenerativeModel(MODEL_ID).start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to start chat session: {e}")
        st.stop()

# Store visible history for display/export
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Streamlit UI ---
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("Gemini Chatbot with Context Memory")

# Text input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask me anything...", key="input")
    submitted = st.form_submit_button("Send")

# Handle message sending
if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))

    try:
        response = st.session_state.chat_session.send_message(user_input)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    st.session_state.chat_history.append(("Gemini", bot_reply))

# Display chat history
st.markdown("### 💬 Chat History")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:**\n\n{message}", unsafe_allow_html=True)

st.divider()

# Download chat history
if st.button("📥 Download Chat Log"):
    if st.session_state.chat_history:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        chat_text = "\n\n".join([f"{sender}: {msg}" for sender, msg in st.session_state.chat_history])
        st.download_button(
            label="Download .txt file",
            data=chat_text,
            file_name=f"gemini_chat_{now}.txt",
            mime="text/plain"
        )
    else:
        st.warning("No chat history to download.")

# Clear chat session
if st.button("🧹 Clear Chat"):
    st.session_state.chat_session = genai.GenerativeModel(MODEL_ID).start_chat(history=[])
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
