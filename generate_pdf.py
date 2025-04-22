from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import validation
import data_preparation

# Function to create a corrected PDF
def create_corrected_pdf(errors, filename="corrected_question_paper.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750
    for section, error in errors.items():
        c.drawString(50, y_position, f"{section}: {error}")
        y_position -= 30

    c.save()
    print("✅ Corrected PDF generated!")

if __name__ == "__main__":
    extracted_text = data_preparation.extract_text_from_pdf("sample_question_paper.pdf")
    extracted_marks = data_preparation.extract_marks(extracted_text)
    errors = validation.validate_marks(extracted_marks)

    if errors:
        create_corrected_pdf(errors)
    else:
        print("✅ No errors found! No correction needed.")
