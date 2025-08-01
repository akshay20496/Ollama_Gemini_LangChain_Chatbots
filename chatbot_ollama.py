import streamlit as st
from langchain_community.chat_models import ChatOllama
from datetime import date

# Streamlit app configuration
st.set_page_config(page_title="ChatBot", page_icon='🤖', layout='centered', initial_sidebar_state='collapsed')

# Initialize session state for history and LLM
if 'history' not in st.session_state:
    st.session_state.history = []

# Use markdown to render the centered header
st.markdown("<h2 style='text-align: center; color: black;background-color: white;border-radius: 10px;'>🤖ChatBot</h2>", unsafe_allow_html=True)

# Initialize session state with model start chat message
if 'llm' not in st.session_state:
    st.session_state.llm = ChatOllama(
        model="llama3.2:1b",
        base_url="http://localhost:11434",
        temperature=0.7
    )

# Initialize session state with todays date
if 'today_date' not in st.session_state:
    st.session_state.today_date = date.today().strftime("%d %B %Y")

# CSS for chat style and background
st.markdown(f"""
<style>
    /* Set the background image for the entire app */
    .stApp {{
        background-image: url("https://i.pinimg.com/736x/29/51/8d/29518df9a720818938a3a58cf6c026df.jpg");
        background-size: 715px;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .user-message {{
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        align-self: flex-end;
        background-color: #dcf8c6;
    }}
    .bot-message {{
    border-radius: 10px;
    align-self: flex-start;
    padding: 10px;
    margin: 5px 0;
    max-width: 80%;
    background-color: #ffffff;
    border: 1px solid #e5e5e5;
            }}
    .chat-date {{
        text-align: center;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100px;
        background-color: #F0F0F0;
        margin: -15px auto;
        padding: 5px;
    }}
    .message-container {{
        display: flex;
        flex-direction: column;
    }}
</style>
""", unsafe_allow_html=True)

# Display the chat history
st.markdown(f'<div class="chat-date" style="align:center;">{st.session_state.today_date}</div>', unsafe_allow_html=True)
for message in st.session_state.history:
    st.markdown(f'<div class="message-container"><div class="user-message">{message["user"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-container"><div class="bot-message">{message["bot"]}</div></div>', unsafe_allow_html=True)

# Function to add message to history
def add_message(user, bot):
    st.session_state.history.append({"user": user, "bot": '🤖\n\n'+bot})

# Function to handle question input and response
def handle_question(question):
    try:
        # Build full chat history as messages
        messages = []
        for msg in st.session_state.history:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["bot"]})

        # Add current question
        messages.append({"role": "user", "content": question})

        # Invoke model with full history
        response = st.session_state.llm.invoke(messages)
        add_message(question, response.content)
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Input box for user questions
question = st.chat_input("Say something")
if question:
    handle_question(question)
    #st.experimental_rerun()
    st.rerun()