import streamlit as st
import requests
import json
from io import StringIO

# Initialize session state
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'generated_cover_letter' not in st.session_state:
    st.session_state.generated_cover_letter = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

st.set_page_config(page_title="Cover Letter Generator", layout="wide")

st.title("Cover Letter Generator")
st.write("Upload your resume and provide a job description to generate tailored documents.")

# Model selection
model_provider = st.radio(
    "Select AI Model Provider",
    ["OpenAI", "GitHub"],
    help="Choose which AI model provider to use for generation"
)

# File upload
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Job description input
job_description = st.text_area("Paste job description here", key="job_description_input")
job_url = st.text_input("Or enter job posting URL (optional)", key="job_url_input")

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Documents"):
        if resume_file is None:
            st.error("Please upload your resume")
        elif not job_description and not job_url:
            st.error("Please provide either a job description or URL")
        else:
            with st.spinner("Generating documents..."):
                try:
                    # Prepare the request
                    files = {"resume": resume_file}
                    data = {
                        "job_description": {
                            "text": job_description,
                            "url": job_url if job_url else None
                        },
                        "model_provider": model_provider
                    }
                    
                    # Make API request
                    response = requests.post(
                        "http://localhost:8000/generate",
                        files=files,
                        data={"job_description": json.dumps(data["job_description"]),
                              "model_provider": model_provider}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Store results in session state
                        st.session_state.generated_resume = result["updated_resume"]
                        st.session_state.generated_cover_letter = result["cover_letter"]
                        st.session_state.show_results = True
                    else:
                        st.error(f"Error generating documents: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

with col2:
    if st.session_state.show_results:
        if st.button("Create New Documents"):
            # Clear session state
            st.session_state.generated_resume = None
            st.session_state.generated_cover_letter = None
            st.session_state.show_results = False
            st.rerun()

# Display results if they exist
if st.session_state.show_results:
    # Create two columns for the results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Updated Resume")
        resume_text = st.text_area("", st.session_state.generated_resume, height=300, key="resume_output")
        # Add copy button for resume
        if st.button("📋 Copy Resume", key="copy_resume"):
            st.write("```python\n" + st.session_state.generated_resume + "\n```")
            st.success("Resume copied to clipboard!")
        # Add download button for resume
        st.download_button(
            "📥 Download Resume",
            st.session_state.generated_resume,
            file_name="updated_resume.txt",
            key="download_resume"
        )
    
    with col2:
        st.subheader("Cover Letter")
        cover_letter_text = st.text_area("", st.session_state.generated_cover_letter, height=300, key="cover_letter_output")
        # Add copy button for cover letter
        if st.button("📋 Copy Cover Letter", key="copy_cover_letter"):
            st.write("```python\n" + st.session_state.generated_cover_letter + "\n```")
            st.success("Cover letter copied to clipboard!")
        # Add download button for cover letter
        st.download_button(
            "📥 Download Cover Letter",
            st.session_state.generated_cover_letter,
            file_name="cover_letter.txt",
            key="download_cover_letter"
        ) 