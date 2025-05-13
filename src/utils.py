from pypdf import PdfReader
import json_repair

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

# try:
#     t = process_pdf(r"E:\DATA SCIENCE\projects\Agents\01-Quiz generator\data\[7] RNN-GRU-LSTM.pdf")
#     print(t)
# except Exception as e:
#     print(f"Error: {str(e)}")

def parse_json(text):
    """Parse JSON content and repair if necessary"""
    try:
        return json_repair.loads(text)
    except:
        return None
    
# to run this : python crew_ai/utils.py