"""
Quiz Generation Pipeline

Orchestrates the process of extracting text from PDFs and generating quiz questions 
using CrewAI agents. Takes a PDF input and produces JSON quiz output.
"""

from src.crew import QuizGeneratorCrew
from src.utils import process_pdf
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
mcq_quiz_file = os.path.join(current_directory, 'output', 'mcq_quiz.json')
tf_quiz_file = os.path.join(current_directory, 'output', 'tf_quiz.json')
analyzer_quiz_file = os.path.join(current_directory, 'output', 'quiz_analysis.json')

def run_pipeline(DATA_PATH):
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
        file=mcq_quiz_file,
        mode='r',
        encoding='utf-8'
    ) as f1, \
        open(
            file=tf_quiz_file,
            mode='r',
            encoding='utf-8'
        ) as f2, \
        open(
            file=analyzer_quiz_file,
            mode='r',
            encoding='utf-8'
        ) as f3:
        mcq_data = f1.read()
        tf_data = f2.read()
        quiz_analysis_data = f3.read()
        return mcq_data, tf_data, quiz_analysis_data


# To Run the code:
# cd
# python src/quiz_pipeline.py
if __name__ == "__main__":
    DATA_PATH = r"E:\Data Science\Projects\crewai\Quiz-Generator\data\Explanation of NLP Embedding Methods.pdf"
    run_pipeline(DATA_PATH)
