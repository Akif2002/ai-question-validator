import fitz  # PyMuPDF
import re
import os

# Define the PDF file path
pdf_path = "sample_question_paper.pdf"

# Check if the file exists before opening it
if not os.path.exists(pdf_path):
    print(f"❌ Error: File '{pdf_path}' not found in directory: {os.getcwd()}")
    exit()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Function to extract marks from the extracted text
def extract_marks(text):
    marks_pattern = r"Section\s+([A-Z])\s*-\s*(\d+)\s*Marks"
    sections = re.findall(marks_pattern, text)
    return {section: int(marks) for section, marks in sections}

# Run extraction
if __name__ == "__main__":
    extracted_text = extract_text_from_pdf(pdf_path)
    marks_dict = extract_marks(extracted_text)

    print("\n✅ Extracted Text:\n", extracted_text)
    print("\n✅ Extracted Marks:", marks_dict)
