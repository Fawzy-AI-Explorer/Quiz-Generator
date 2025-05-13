"""
Quiz Generation Pipeline

Orchestrates the process of extracting text from PDFs and generating quiz questions 
using CrewAI agents. Takes a PDF input and produces JSON quiz output.
"""

from crew import QuizGeneratorCrew
from utils import process_pdf
from config.config import DATA_PATH


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


# To Run the code: 
# cd 
# python src/quiz_pipeline.py