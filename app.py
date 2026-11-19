import os
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Article Summarizer & Q&A", page_icon="🤖")

st.title("🤖 AI Article Summarizer & Q&A")
st.write("Paste any article, notes, or text below to get an instant AI breakdown and key takeaways!")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    os.environ["GEMINI_API_KEY"] = api_key.strip()

text_input = st.text_area("Paste your text or article here:", height=250)

if st.button("Summarize Text", type="primary"):
    if not api_key and "GEMINI_API_KEY" not in os.environ:
        st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    elif not text_input.strip():
        st.error("Please paste some text first.")
    else:
        with st.spinner("Generating summary with Gemini..."):
            try:
                client = genai.Client(api_key=api_key.strip())
                prompt = (
                    "Analyze the following text and provide:\n"
                    "1. Executive Summary\n"
                    "2. Key Bullet Points\n"
                    "3. Actionable Takeaways\n\n"
                    f"Text:\n{text_input}"
                )
                models_to_try = [
                    "gemini-3.5-flash-lite",
                    "gemini-3.1-flash-lite",
                    "gemini-3.8-flash",
                ]
                response = None
                last_error = None

                for raw_model in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=raw_model.strip(),
                            contents=prompt,
                        )
                        if getattr(response, "text", None):
                            break
                    except Exception as model_err:
                        last_error = model_err
                        continue

                if not response or not getattr(response, "text", None):
                    raise last_error or RuntimeError("No response returned from Gemini.")

                st.success("Summary Ready!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
