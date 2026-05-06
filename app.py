import streamlit as st
from dotenv import load_dotenv
import os
import time
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Streamlit UI configuration
st.set_page_config(page_title="Fridge Hero 🍳", page_icon=":fried_egg:", layout="centered")
st.title("Fridge Hero 🍳")

st.markdown(
    """
    <style>
    textarea, input {
        font-size: 1.1rem !important;
    }
    .stButton>button {
        background-color: #fadb6a;
        color: #45260a;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 8px;
        padding: 0.45em 1.7em;
    }
    .stButton>button:hover {
        background: #ffe08f;
        color: #a56709;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Three input fields for ingredients
ing1 = st.text_input("Ingredient 1")
ing2 = st.text_input("Ingredient 2")
ing3 = st.text_input("Ingredient 3")

cook = st.button("Cook Magic ✨")

if cook:
    if not (GEMINI_API_KEY and ing1 and ing2 and ing3):
        st.warning("Please enter all three ingredients and check your API key in the .env file.")
    else:
        prompt = (
            f"You are a creative chef. Using {ing1}, {ing2}, {ing3}, "
            "provide a French-inspired dish name and 3 simple cooking steps."
        )
        # Respect Gemini free tier rate limit
        with st.spinner("✨ Cooking up some inspiration..."):
            time.sleep(4)
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                recipe = response.text if hasattr(response, "text") else str(response)
                with st.container():
                    st.success(recipe)
            except Exception as e:
                st.error(f"Failed to fetch recipe: {e}", icon="🚫")