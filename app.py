import os
import streamlit as st
from google import genai

# Page setup
st.title("🤖 AI Article Summarizer & Q&A")
st.markdown("Paste any article, notes, or text below to get an instant AI breakdown and key takeaways!")

# Sidebar for API Key
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

# Text input box
text_input = st.text_area("Paste your text or article here:", height=250)

if st.button("Summarize Text", type="primary"):
    if not api_key and "GEMINI_API_KEY" not in os.environ:
        st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    elif not text_input:
        st.error("Please paste some text first.")
    else:
        with st.spinner("Generating summary with Gemini..."):
            try:
                client = genai.Client()
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"Analyze the following text and provide:\n1. Executive Summary\n2. Key Bullet Points\n3. Actionable Takeaways\n\nText:\n{text_input}"
                )
                
                st.success("Summary Ready!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
