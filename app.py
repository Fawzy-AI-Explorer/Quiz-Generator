"""
Quiz Generator Web Application

A Streamlit app that generates multiple-choice quizzes from input text.
Uses a pipeline to process text and create questions.
"""

import json
import streamlit as st
from src.quiz_pipeline import run_pipeline

import sqlite3
print(sqlite3.sqlite_version)
import sys
import chromadb
import crewai
import streamlit
import numpy
print("Python version:", sys.version)
print("ChromaDB version:", chromadb.__version__)
print("CrewAI version:", crewai.__version__)
print("Streamlit version:", streamlit.__version__)
print("NumPy version:", numpy.__version__)

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


def format_quiz_output(json_data_mcq, json_data_tf, json_data_analysis):
    """Format quiz JSON data into HTML output for MCQ and True/False questions.

    Args:
        json_data_mcq (dict): JSON data containing MCQ quiz questions with topic and quiz items
        json_data_tf (dict): JSON data containing True/False
                             quiz questions with topic and quiz items

    Returns:
        tuple: A tuple containing two strings (mcq_output, tf_output)
               with formatted HTML for both quiz types.
            Returns None if required JSON structure is invalid.

    The function expects JSON data in the following format:
    {
        "topic": "Quiz Topic",
        "quiz": [
            {
                "question": "Question text",
                "options": ["Option 1", "Option 2", ...]
            },
            ...
        ]
    }
    """

    # MCQ Quiz
    if "quiz" not in json_data_mcq or "topic" not in json_data_mcq:
        return None

    topic = json_data_mcq["topic"]
    quiz_items = json_data_mcq["quiz"]

    mcq_output = f'<div class="quiz-title">Quiz on {topic}</div>'

    for idx, item in enumerate(quiz_items, 1):
        question_html = f'<div class="quiz-container">'
        question_html += f'<div class="quiz-question">Q{idx}: {item["question"]}</div>'
        for opt_idx, option in enumerate(item["options"], 0):
            question_html += (
                f'<div class="quiz-option">{"abcd"[opt_idx]}. {option}</div>'
            )
        question_html += "</div>"
        mcq_output += question_html

    # TF Quiz
    if "quiz" not in json_data_tf:
        return None

    quiz_items = json_data_tf["quiz"]

    tf_output = f'<div class="quiz-title">Quiz on {topic}</div>'

    for idx, item in enumerate(quiz_items, 1):
        question_html = f'<div class="quiz-container">'
        question_html += f'<div class="quiz-question">Q{idx}: {item["question"]}</div>'
        for opt_idx, option in enumerate(item["options"], 0):
            question_html += (
                f'<div class="quiz-option">{"abcd"[opt_idx]}. {option}</div>'
            )
        question_html += "</div>"
        tf_output += question_html

    # Quiz Analysis
    if "quiz" not in json_data_analysis:
        return None

    quiz_items = json_data_analysis["quiz"]

    analysis_output = f'<div class="quiz-title">Quiz on {topic}</div>'

    for idx, item in enumerate(quiz_items, 1):
        question_html = f'<div class="quiz-container">'
        question_html += f'<div class="quiz-question">Question Explanation: {item["Question_Explanation"]}</div>'
        question_html += f'<div class="quiz-question">Answer Feedback: {item["Answer_Feedback"]}</div>'
        question_html += f'<div class="quiz-question">Correct Answer: {item["Correct_Answer"]}</div>'
        question_html += f'<div class="quiz-question">Related Topics: {item["Related_Topics"]}</div>'
        question_html += "</div>"
        analysis_output += question_html

    return mcq_output, tf_output, analysis_output


def format_quiz_text(json_data_mcq, json_data_tf):
    """Format quiz JSON into plain text for download."""
    if "quiz" not in json_data_mcq or "topic" not in json_data_mcq:
        return None

    topic = json_data_mcq["topic"]
    quiz_items = json_data_mcq["quiz"]

    output = f"Quiz on {topic}\n\n"
    output = f"MCQ Questions\n\n"

    for _, item in enumerate(quiz_items, 1):
        output += f"Question: {item['question']}\n"
        for _, option in enumerate(item["options"], 0):
            output += f"{option}\n"
        output += "\n"

    if "quiz" not in json_data_tf or "topic" not in json_data_tf:
        return None

    quiz_items = json_data_tf["quiz"]

    output = f"T/F Questions\n\n"

    for _, item in enumerate(quiz_items, 1):
        output += f"Question: {item['question']}\n"
        for _, option in enumerate(item["options"], 0):
            output += f"{option}\n"
        output += "\n"

    return output


def main():
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

    # Display results if JSON output exists
    if st.session_state.json_output is not None:
        st.subheader("Processing Results")
        st.success("PDF processed successfully!")

        try:
            mcq_json_out = st.session_state.json_output[0]
            tf_json_out = st.session_state.json_output[1]
            analysis_json_out = st.session_state.json_output[2]
            mcq_parsed_json = json.loads(mcq_json_out)
            tf_parsed_json = json.loads(tf_json_out)
            analysis_parsed_json = json.loads(analysis_json_out)

            # Format JSON output for display
            mcq_formatted_output, tf_formatted_output, analysis_formatted_output = format_quiz_output(
                mcq_parsed_json, tf_parsed_json, analysis_parsed_json
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
