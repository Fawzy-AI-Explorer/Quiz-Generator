from crew import QuizGeneratorCrew
from utils import process_pdf
from config.config import DATA_PATH

# from crew import get_crew



try:
    # Process PDF
    txt = process_pdf(DATA_PATH)
    print(f"PDF content extracted successfully!")
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