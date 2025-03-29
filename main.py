# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:21:05 2025

@author: Sudarshan Systems
"""

import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai  # ✅ Correct import

# Load environment variables
load_dotenv(".env.txt")

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

# Get Google API Key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Ensure API key is loaded
if not GOOGLE_API_KEY:
    st.error("API Key is missing! Please check your .env file.")
    st.stop()

# Configure Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)

# ✅ Check available models (Run once to verify)
try:
    available_models = [model.name for model in gen_ai.list_models()]
    st.write("Available Models:", available_models)  # Optional: Show models for debugging
except Exception as e:
    st.error(f"Error fetching models: {e}")
    st.stop()

# ✅ Set the correct model name (Change if needed)
MODEL_NAME = "gemini-1.5-pro"  # Replace with the correct model name from the above list

try:
    model = gen_ai.GenerativeModel(MODEL_NAME)  # ✅ Correct reference
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Function to translate roles for Streamlit display
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# ✅ Initialize chat session only if not already created
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("🤖 ChatBuddy-Ready to Assist")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text if hasattr(message.parts[0], "text") else message.parts[0])

# User input
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Error processing response: {e}")
