"""
Quiz Generator Web Application

A Streamlit app that generates multiple-choice quizzes from input text.
Uses a pipeline to process text and create questions.
DONE✅
"""

import sys
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    print("pysqlite3 not installed, falling back to default sqlite3")
import sqlite3
print(f"SQLite version: {sqlite3.sqlite_version}")
print(f"SQLite module path: {sqlite3.__file__}")


import json
import streamlit as st
from src.quiz_pipeline import run_pipeline
from src.utils import format_quiz_output, format_quiz_text

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stFileUploader {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
    }
    .quiz-container {
        background-color: #ffffff;
        border: 2px solid #d1d5db;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .quiz-question {
        font-size: 18px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 10px;
    }
    .quiz-option {
        font-size: 16px;
        color: #374151;
        margin: 5px 0;
    }
    .quiz-title {
        font-size: 24px;
        font-weight: bold;
        color: #f6d55c;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def main():
    """Main Streamlit application function.

    This function handles:
    1. Initializing session state variables for file uploads and outputs
    2. Setting up the main UI components including title and sidebar
    3. Processing uploaded PDFs through the quiz generation pipeline
    4. Displaying formatted quiz results and analysis

    The app allows users to:
    - Upload PDF files
    - Generate MCQ and True/False questions
    - View detailed question analysis
    - Download quiz content

    Returns:
        None
    """
    # Initialize session state variables
    if "uploaded_file_content" not in st.session_state:
        st.session_state.uploaded_file_content = None
    if "json_output" not in st.session_state:
        st.session_state.json_output = None
    if "upload_time" not in st.session_state:
        st.session_state.upload_time = None

    # App header
    st.title("📄 Quiz Generator")
    st.markdown(
        """
    Welcome to Quiz Generator! Upload your PDF file, and our app will generate a quiz based on the file.
    """
    )

    # Sidebar
    with st.sidebar:
        st.header("Upload Your PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file", type=["pdf"], accept_multiple_files=False
        )

    # Main content
    if uploaded_file is not None:

        # Update session state
        st.session_state.upload_time = st.session_state.get("upload_time", "")

        # Process the uploaded file
        with st.spinner("Processing PDF..."):
            # Reset file pointer to start for run_pipeline
            uploaded_file.seek(0)
            st.session_state.json_output = run_pipeline(uploaded_file)
            print(f"st.session_state.json_output: {st.session_state.json_output}")

    # Display results if JSON output exists
    if st.session_state.json_output is not None:
        st.subheader("Processing Results")
        st.success("PDF processed successfully!")

        try:
            mcq_json_out = st.session_state.json_output[0]
            print(f"mcq_json_out: {mcq_json_out}")
            tf_json_out = st.session_state.json_output[1]
            print(f"tf_json_out: {tf_json_out}")
            analysis_json_out = st.session_state.json_output[2]
            print(f"analysis_json_out: {analysis_json_out}")
            mcq_parsed_json = json.loads(mcq_json_out)
            print(f"mcq_parsed_json: {mcq_parsed_json}")
            tf_parsed_json = json.loads(tf_json_out)
            print(f"tf_parsed_json: {tf_parsed_json}")
            analysis_parsed_json = json.loads(analysis_json_out)
            print(f"analysis_parsed_json: {analysis_parsed_json}")

            # Format JSON output for display
            mcq_formatted_output, tf_formatted_output, analysis_formatted_output = (
                format_quiz_output(
                    mcq_parsed_json, tf_parsed_json, analysis_parsed_json
                )
            )

            # Display mcq formatted quiz
            if mcq_formatted_output:
                st.markdown("### Generated MCQ Quiz Content")
                st.markdown(mcq_formatted_output, unsafe_allow_html=True)
            # Display tf formatted quiz
            if tf_formatted_output:
                st.markdown("### Generated T/F Quiz Content")
                st.markdown(tf_formatted_output, unsafe_allow_html=True)
            # Display tf formatted quiz
            if analysis_formatted_output:
                st.markdown("### Generated Quiz Analysis Content")
                st.markdown(analysis_formatted_output, unsafe_allow_html=True)

            # # Generate plain text for download
            # quiz_text = format_quiz_text(mcq_parsed_json, tf_parsed_json)
            # if quiz_text:
            #     st.download_button(
            #         label="Download Quiz",
            #         data=quiz_text,
            #         file_name="quiz.txt",
            #         mime="text/plain",
            #         key="download_quiz",
            #     )
            # else:
            #     st.warning("No quiz data found in the processed PDF.")
        except json.JSONDecodeError:
            st.error(
                "Error: Unable to parse quiz data. The extracted content is not valid JSON."
            )

    else:
        st.info("Please upload a PDF file to begin processing.")


if __name__ == "__main__":
    main()