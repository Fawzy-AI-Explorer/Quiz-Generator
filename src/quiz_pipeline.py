"""
Quiz Generation Pipeline

Orchestrates the process of extracting text from PDFs and generating quiz questions 
using CrewAI agents. Takes a PDF input and produces JSON quiz output.
"""

from src.crew import QuizGeneratorCrew
from src.utils import process_pdf


def run_pipeline(DATA_PATH):
    """
    Run the quiz generation pipeline.
    Args:
        DATA_PATH (str): Path to the PDF file to be processed.
    Returns:
        tuple: Contains two JSON strings:
            - mcq_data: JSON string of multiple-choice questions
            - tf_data: JSON string of true/false questions
    """
    try:
        # Process PDF
        txt = process_pdf(DATA_PATH)
        print("PDF content extracted successfully!")
        # print(txt)
        # Initialize and run crew
        inputs = {
            "text": txt
        }
        generator = QuizGeneratorCrew()
        result = generator.kickoff(inputs=inputs)
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise
    with open(
        file=r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\output\mcq_quiz.json',
        mode='r',
        encoding='utf-8'
    ) as f1, \
        open(
            file=r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\output\tf_quiz.json',
            mode='r',
            encoding='utf-8'
        ) as f2:
        mcq_data = f1.read()
        tf_data = f2.read()
        return mcq_data, tf_data


# To Run the code:
# cd
# python src/quiz_pipeline.py
