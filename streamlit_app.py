import streamlit as st
from chatbot.config import chatbot
from chatbot.pizza_functions import PizzaFunctions
import google.generativeai as genai




# Load API key securely: from Streamlit secrets or local .env
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    PizzaFunctions.clear_orders()


st.title("🍕 PizzaBot Ordering Assistant")

user_input = st.chat_input("Say something to PizzaBot...")

if user_input:
    with st.spinner("PizzaBot is typing..."):
        response = chatbot.get_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))


for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
