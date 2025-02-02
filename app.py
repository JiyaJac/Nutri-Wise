# app.py (Streamlit frontend)
# app.py (Streamlit frontend)
import streamlit as st
import requests
import google.generativeai as genai

st.markdown(
    """
    <style>
        .stApp {
            background-color: #4a90e2; /* Light Blue */
        }
    </style>
    """,
    unsafe_allow_html=True
)

genai.configure(api_key="AIzaSyDhge203wnvNPMrkCaf76Miy8l4xraXv5E")
model = genai.GenerativeModel("gemini-1.5-flash")

# URL of your Django API (update with your server's URL)
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDhge203wnvNPMrkCaf76Miy8l4xraXv5E"  # Update with the correct Django URL

# Streamlit UI
st.title("Google Gemini AI Prompt App")
st.write("Enter a prompt and get a response from Google Gemini!")

# User input (prompt for AI)
user_prompt = st.text_input("Enter your prompt:")

prompt = user_prompt



if st.button("Get AI Response"):
    if user_prompt and len(prompt)!=0:
        response = model.generate_content(prompt)
        st.write(response.text)
        
    
    else:
        st.warning("Please enter a prompt.")
st.markdown("---")  # Adds a horizontal separator

st.subheader("Nutrition Calculator")
st.write("Click the button below to access the nutrition calculator.")

if st.button("Go to Nutrition Calculator"):
    st.switch_page("pages/nutrition.py")



