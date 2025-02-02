# app.py (Streamlit frontend)
import streamlit as st
import requests
import google.generativeai as genai


genai.configure(api_key="AIzaSyDhge203wnvNPMrkCaf76Miy8l4xraXv5E")
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("Retrieve recommended meal recipes as per your calorie requirements: ")
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
