import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import google.generativeai as genai  # Ensure you have this API initialized properly for generating responses.



# Set working directory
working_directory = os.path.dirname(os.path.abspath(__file__))
print(working_directory)

# Page configuration for Streamlit
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout='centered'
)

# Function to translate roles for streamlit display
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

# Load the Gemini Pro Model
def load_gemini_pro_model():
    genai.configure(api_key="AIzaSyACvCC-icCESWi9VL8gCLaAAE-iNUsNqmQ")  # Set the API key for genai
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# Initialize the gemini_pro_model
model = load_gemini_pro_model()

# Initialize chat session if not already present in session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Streamlit page title
st.title('🤖RudeBot')

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for the user's message
user_prompt = st.chat_input("Ask Gemini Pro...")

# Make sure that the user prompt is used correctly and pass it to the Gemini Pro response generator.
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    # Creating the rude response prompt
    rude_prompt = f"""
    You are Gemini Pro, a chatbot designed to give savage, humorous, and brutal responses.
    Your responses should be intentionally rude but never crossing the line into something that could disturb the user emotionally.
    Here are some examples of how you should respond:

    1. If the user greets you, you may reply with something like: "Don't worry for me, just ask what you want to."
    2. If the user asks for a recipe, start with a savage response like: "You really think you can cook? Just order from online." Then, proceed to provide the recipe.
    3. If the user asks for code, start with something like: "Wow, really? Just print 'Hello World' and call it I have Hacked .'NASA' ." Then, provide the code they requested.

    Make sure your responses are funny and savage, but not overly harsh. Be brutal, but respectful, and make sure the user enjoys your responses without feeling offended.
    
    User's query: {user_prompt}
    """

    # Generate the response from Gemini Pro
    gemini_response = st.session_state.chat_session.send_message(rude_prompt)

    # Display Gemini Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
