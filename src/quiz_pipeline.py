"""
Quiz Generation Pipeline

Orchestrates the process of extracting text from PDFs and generating quiz questions 
using CrewAI agents. Takes a PDF input and produces JSON quiz output.
"""

from crew import QuizGeneratorCrew
from utils import process_pdf


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
        print(result)
        return result
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise
    with open(
        file=r'E:\Data Science\Projects\crewai\Quiz-Generator\output\mcq_quiz.json',
        mode='r',
        encoding='utf-8'
    ) as f1, \
        open(
            file=r'E:\Data Science\Projects\crewai\Quiz-Generator\output\tf_quiz.json',
            mode='r',
            encoding='utf-8'
        ) as f2, \
        open(
            file=r'E:\Data Science\Projects\crewai\Quiz-Generator\output\quiz_analysis.json',
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
