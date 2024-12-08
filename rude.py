import os
import streamlit as st
import google.generativeai as genai
from datetime import datetime

def apply_custom_css():
    """Apply custom styling to enhance UI/UX."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', sans-serif;
        }
        
        .chat-message {
            padding: 1rem;
            border-radius: 1rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .user-message {
            background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .bot-message {
            background: linear-gradient(to right, #00b4db 0%, #0083b0 100%);
            color: white;
        }
        
        .stButton>button {
            background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
            color: white;
            border-radius: 1rem;
            font-weight: 600;
            transition: transform 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
        }
        
        .main-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(45deg, #6c5ce7, #a88beb);
            color: white;
            border-radius: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        
        .error-message {
            background-color: #ffe0e0;
            border-left: 5px solid #ff6b6b;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def handle_safety_error(error_str):
    """Handle potential safety errors with humorous responses."""
    safety_responses = [
        "😅 Oops! Looks like my comedy circuit got a bit tangled.",
        "🚫 Whoa, that request just broke my joke generator!",
        "🤖 Error 404: Savage response not found. Try again!",
        "🛡️ Nice try, but my humor firewall just blocked that request!"
    ]
    return safety_responses[hash(error_str) % len(safety_responses)]

def generate_savage_response(user_query, savage_level):
    """Generate a humorous, savage response with respect and no hatefulness."""
    
    savage_styles = {
        "low": {
            "tone": "Lightly sarcastic",
            "style": "Friendly teasing with a touch of humor"
        },
        "medium": {
            "tone": "Playfully cheeky",
            "style": "Clever roasts with a humorous twist"
        },
        "high": {
            "tone": "Boldly sarcastic",
            "style": "Sharp wit, no malice, just fun"
        }
    }

    # Determine savage category
    savage_category = "low" if savage_level <= 1 else "medium" if savage_level <= 2 else "high"

    try:
        # Predefined savage prompt
        savage_prompt = f"""
        You are Gemini Pro, a chatbot designed to give savage, humorous, and fun responses. 
        Your responses should not be intentionally rude but should balance sass and respect.
        Ensure all responses are concise and in alignment with the savage level provided.

        Context:
        - Savage Level: {savage_level}/3
        - Current Tone: {savage_styles[savage_category]['tone']}
        - Response Style: {savage_styles[savage_category]['style']}

        User Query: {user_query}

        Respond with a single, clever, and unexpected savage remark, followed by a helpful or kind note if relevant
        for example :
        
        1. If the user greets you, reply with something like: "Don't worry, just ask what you want already."
        2. If the user asks for a recipe, start with a savage response like: "You really think you can cook? Just order from online." Then, proceed to provide the recipe.
        3. If the user asks for code, start with something like: "Wow, really? Just print 'Hello World' and call it a day." Then, provide the code they requested.
        4.If the user asks for information about anything may strat with with roasting him with positive way like "All the time you AI helps you why you dont search it yourself and give requested code .
        5.If someone ask for what is your name then you might reply havent you see the title ,i am  Rudebot
        These are only example for reference you can other funny and hilarious responses  with your knowledge, and don't give any negative responses.
        Follow the tips strcitly and compuslsory:
        Be original. Don't just copy what other people are doing.
        Be clever. Your responses should be witty and unexpected.
        Be concise. Don't ramble on and on.
        Be respectful. Don't cross the line into being offensive.
        .
        """

        response = gemini_pro_model.generate_content(savage_prompt)
        return response.text.strip()
    except Exception as e:
        return handle_safety_error(str(e))

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0

# Configure API key and model
API_KEY = "AIzaSyACvCC-icCESWi9VL8gCLaAAE-iNUsNqmQ"  # Set your API key here
genai.configure(api_key=API_KEY)
gemini_pro_model = genai.GenerativeModel("gemini-pro")

def main():
    initialize_session_state()
    apply_custom_css()

    st.markdown("""
        <div class="main-header">
            <h1>🤖 RudeBot: Your Savage Comedy Companion</h1>
            <p>Roasting With Love, Serving Humor With a Twist 😈</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🎮 RudeBot Controls")

        st.markdown("### 🎭 Savage Meter")
        savage_description = {
            1: "🥺 Barely Savage (Friendly Mode)",
            2: "😏 Moderately Savage",
            3: "🔥 Ultimate Savage Overdrive!"
        }

        savage_level = st.slider(
            "How Savage Should I Be?", 
            1, 3, 2, 
            help="Slide to control my savage comedy level!"
        )

        st.info(savage_description[min(max(savage_level, 1), 3)])

        st.markdown("### 📊 Roast Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Roasts Delivered", st.session_state.message_count)
        with col2:
            st.metric("Time", datetime.now().strftime("%H:%M"))

        if st.button("🔄 Reset Roast History", type="primary"):
            st.session_state.chat_history = []
            st.session_state.message_count = 0

    user_prompt = st.chat_input("Dare to chat with the Savage Bot? Type your message... 😈")

    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f'<div class="chat-message user-message">👤 You: {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 RudeBot: {message}</div>', unsafe_allow_html=True)

    if user_prompt:
        with st.spinner("🤖 Charging savage comedy cannons..."):
            st.session_state.chat_history.append(("user", user_prompt))
            response = generate_savage_response(user_prompt, savage_level)
            st.session_state.chat_history.append(("assistant", response))
            st.session_state.message_count += 1

        st.rerun()

if __name__ == "__main__":
    main()
