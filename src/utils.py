"""Utility functions for PDF processing, JSON handling, and file operations"""

import os
import shutil
from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError
from config.config import OUTPUT_PATH


def process_pdf(file_path: str) -> str:
    """Process a PDF file and extract its text content.

    Args:
        file_path (str): Path to the PDF file to process

    Returns:
        str: Extracted text content from the PDF, or error message if processing fails

    Raises:
        PdfReadError: If there is an error reading the PDF file
        PdfStreamError: If there is an error processing the PDF stream
        FileNotFoundError: If the PDF file is not found
        PermissionError: If there are insufficient permissions to read the file
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except (PdfReadError, PdfStreamError) as e:
        return f"Error reading PDF: {str(e)}"
    except FileNotFoundError:
        return "Error: PDF file not found"
    except PermissionError:
        return "Error: Permission denied to access PDF file"


def create_output_dir():
    """Create or recreate the output directory.

    This function manages the output directory by:
    1. Removing the existing directory if it exists
    2. Creating a fresh empty directory

    Returns:
        None

    Raises:
        OSError: If directory creation/deletion fails
        PermissionError: If there are insufficient permissions
    """
    try:
        if os.path.exists(OUTPUT_PATH):
            shutil.rmtree(OUTPUT_PATH)

        os.mkdir(OUTPUT_PATH)
        print("Output Path Created Successfully!")
    except PermissionError as e:
        raise PermissionError(
            f"Permission denied when creating output directory: {e}"
        ) from e
    except OSError as e:
        raise OSError(f"Failed to create output directory: {e}") from e


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
    print(f"\n------ISIDE FORMAT (0):----------\n")
    # MCQ Quiz
    if "quiz" not in json_data_mcq or "topic" not in json_data_mcq:
        return None
    print(f"\n------ISIDE FORMAT (1):----------\n")

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
    print(f"\n------ISIDE FORMAT (2):----------\n")

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
    print(f"\n------ISIDE FORMAT (3):----------\n")

    quiz_items = json_data_analysis["quiz"]

    analysis_output = f'<div class="quiz-title">Quiz on {topic}</div>'

    for idx, item in enumerate(quiz_items, 1):
        question_html = f'<div class="quiz-container">'
        question_html += f'<div class="quiz-question">Question Explanation: {item["Question_Explanation"]}</div>'
        question_html += f'<div class="quiz-question">Answer Feedback: {item["Answer_Feedback"]}</div>'
        question_html += (
            f'<div class="quiz-question">Correct Answer: {item["Correct_Answer"]}</div>'
        )
        question_html += (
            f'<div class="quiz-question">Related Topics: {item["Related_Topics"]}</div>'
        )
        question_html += "</div>"
        analysis_output += question_html

    return mcq_output, tf_output, analysis_output


def format_quiz_text(json_data_mcq, json_data_tf):
    """Format quiz data into plain text output.

    Takes MCQ and True/False quiz JSON data and formats it into a readable text format
    with questions and options listed sequentially.

    Args:
        json_data_mcq (dict): JSON data containing MCQ quiz questions and topic
        json_data_tf (dict): JSON data containing True/False quiz questions and topic

    Returns:
        str: Formatted quiz text with MCQ and T/F questions, or None if JSON data is invalid
    """
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
