from pypdf import PdfReader
import json_repair
import os
import shutil


def process_pdf(file_path: str) -> str:
    """Extract text content from PDF files"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def parse_json(text):
    """Parse JSON content and repair if necessary"""
    try:
        return json_repair.loads(text)
    except:
        return None

def create_output_dir(OUTPUT_PATH):
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)

    os.mkdir(OUTPUT_PATH)
    print("Output Path Created Successfully!")


# to run this : python crew_ai/utils.py
