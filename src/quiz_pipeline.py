"""
Quiz Generation Pipeline

Orchestrates the process of extracting text from PDFs and generating quiz questions
using CrewAI agents. Takes a PDF input and produces JSON quiz output.
"""

import os
from src.crew import QuizGeneratorCrew
from src.utils import process_pdf
from config.config import DATA_PATH, OUTPUT_PATH, RUNNING


def run_pipeline(data_path):
    """Run the quiz generation pipeline.

    This function orchestrates the complete quiz generation process:
    1. Extracts text content from the input PDF
    2. Initializes the CrewAI agents and tasks
    3. Generates MCQ and True/False questions
    4. Produces detailed quiz analysis

    Args:
        data_path (str): Path to the input PDF file

    Returns:
        If RUNNING == "LOCAL":
            dict: Raw output from CrewAI agents containing generated quiz content
        If RUNNING == "SERVER":
            tuple: (mcq_json, tf_json, analysis_json) strings containing the quiz data

    Raises:
        Exception: If PDF processing or quiz generation fails
        ValueError: If RUNNING environment is not 'SERVER' or 'LOCAL'
    """
    try:
        # Process PDF
        txt = process_pdf(data_path)
        print("PDF content extracted successfully!")
        # Initialize and run crew
        inputs = {"text": txt}
        generator = QuizGeneratorCrew()
        result = generator.kickoff(inputs=inputs)
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise

    if RUNNING == "SERVER":
        task_results = [None, None, None]

        for result in result.tasks_output:
            if result.name == "MCQ Quiz Generate":
                task_results[0] = result.raw
            elif result.name == "True False Quiz Generate":
                task_results[1] = result.raw
            elif result.name == "Quiz Questions Analysis":
                task_results[2] = result.raw
            else:
                raise NameError(f"Unknown task name {result.name}")

        return task_results

    if RUNNING == "LOCAL":
        try:
            with open(
                file=os.path.join(OUTPUT_PATH, "mcq_quiz.json"),
                mode="r",
                encoding="utf-8",
            ) as f1, open(
                file=os.path.join(OUTPUT_PATH, "tf_quiz.json"),
                mode="r",
                encoding="utf-8",
            ) as f2, open(
                file=os.path.join(OUTPUT_PATH, "quiz_analysis.json"),
                mode="r",
                encoding="utf-8",
            ) as f3:
                mcq_data = f1.read()
                tf_data = f2.read()
                quiz_analysis_data = f3.read()
                return mcq_data, tf_data, quiz_analysis_data
        except Exception as e:
            raise RuntimeError(f"Failed to read quiz output files: {e}") from e
    else:
        raise ValueError(
            "Error: RUNNING Environment muse be ('SERVER' or 'LOCAL')"
            "Please update in config.py file"
        )


if __name__ == "__main__":
    result = run_pipeline(DATA_PATH)
    print(result)
