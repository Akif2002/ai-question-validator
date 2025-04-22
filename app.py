import re

def validate_paper(content):
    errors = []
    warnings = []
    
    # Extract declared section marks (e.g., "Section A - 20 Marks")
    section_match = re.search(r"Section\s+[A-Z]\s*-\s*(\d+)\s*Marks", content, re.IGNORECASE)
    declared_marks = int(section_match.group(1)) if section_match else None

    # Extract questions with marks (e.g., "1. What is AI? (5 Marks)")
    questions = re.findall(r"(\d+)\.\s*(.*?)\((\d+)\s*Marks?\)", content)

    if not questions:
        errors.append("No valid questions detected! Please check the format.")
        return {"errors": errors, "warnings": warnings}

    calculated_marks = sum(int(q[2]) for q in questions)
    
    # ✅ Check for mark distribution mismatch
    if declared_marks and calculated_marks != declared_marks:
        errors.append(f"Mark distribution error! Declared: {declared_marks}, Calculated: {calculated_marks}")

    # ✅ Detect missing question numbers
    question_numbers = [int(q[0]) for q in questions]
    expected_numbers = list(range(1, max(question_numbers) + 1))
    
    missing_numbers = set(expected_numbers) - set(question_numbers)
    if missing_numbers:
        errors.append(f"Missing question numbers: {sorted(missing_numbers)}")

    # ✅ Detect duplicate questions
    question_texts = [q[1].strip().lower() for q in questions]
    duplicates = {q for q in question_texts if question_texts.count(q) > 1}

    if duplicates:
        warnings.append(f"Duplicate questions found: {', '.join(duplicates)}")

    return {"errors": errors, "warnings": warnings}
