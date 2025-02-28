import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client with the API key
client = Groq(api_key=api_key)

# Function to get the response from Groq's LLaMA model
def get_groq_response(user_input: str):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Streamlit UI setup
st.set_page_config(page_title="Groq Chatbot", page_icon=":robot:", layout="wide")  # Set custom page icon

# Title and description
st.title("Groq Chatbot 🤖")
st.subheader("Ask me anything and I'll provide insights using Groq's LLaMA Model.")
st.write("Welcome to the Groq-powered chatbot! Feel free to ask me any question.")

# Initialize session state to hold conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add "Clear Chat" and "New Chat" buttons
col1, col2 = st.columns([1, 1])
with col1:
    clear_button = st.button("Clear Chat", key="clear_chat")
with col2:
    new_chat_button = st.button("New Chat", key="new_chat")

# Handle the button actions
if clear_button:
    st.session_state.messages = []
    st.write("Chat cleared!")

if new_chat_button:
    st.session_state.messages = []
    st.write("Starting a new chat...")

# Display previous messages with formatting
st.markdown("### Conversation History")
for message in st.session_state.messages:
    if message.startswith("You:"):
        st.markdown(f"**You:** {message[4:]}")
    else:
        st.markdown(f"**Bot:** {message[5:]}")

# User input text box with styling
user_input = st.text_input("You: ", "", key="input")

if user_input:
    # Append user's message to session state (conversation history)
    st.session_state.messages.append(f"You: {user_input}")

    # Get the bot's response
    bot_reply = get_groq_response(user_input)

    # Formatting bot's response to look structured with bullet points (if relevant)
    bot_reply = f"**Bot Response:**\n\n{bot_reply}"

    # Example of structured response formatting (add bullet points if the model returns structured information)
    if "important" in bot_reply.lower():  # Example condition for structured response
        bot_reply += "\n\nHere's why fast language models are important:"
        bot_reply += "\n- They process data faster"
        bot_reply += "\n- They enable quicker insights"
   
