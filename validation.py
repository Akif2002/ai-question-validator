import streamlit as st
import re  # Ensure regex is imported

def validate_paper(content):
    st.write("🔎 Debug: Inside validate_paper function")  # Step 1: Check if function runs

    errors = []
    warnings = []

    # Extract declared marks (e.g., "Section A - 20 Marks")
    section_match = re.search(r"Section\s+[A-Z]\s*-\s*(\d+)\s*Marks", content, re.IGNORECASE)
    declared_marks = int(section_match.group(1)) if section_match else None
    st.write(f"📌 Debug: Declared Marks = {declared_marks}")  # Step 2: See if marks are extracted

    # Extract questions with marks (e.g., "1. What is AI? (5 Marks)")
    questions = re.findall(r"(\d+)\.\s*(.*?)\((\d+)\s*Marks?\)", content)
    st.write(f"📌 Debug: Extracted Questions = {questions}")  # Step 3: Check if questions are found

    if not questions:
        errors.append("❌ No valid questions detected! Please check the format.")
        return {"errors": errors, "warnings": warnings}

    calculated_marks = sum(int(q[2]) for q in questions)
    st.write(f"📌 Debug: Calculated Marks = {calculated_marks}")  # Step 4: Verify total marks

    # ✅ Check for mark distribution mismatch
    if declared_marks and calculated_marks != declared_marks:
        errors.append(f"❌ Mark distribution error! Declared: {declared_marks}, Calculated: {calculated_marks}")

    st.write(f"📌 Debug: Errors = {errors}")  # Step 5: Check errors before returning
    return {"errors": errors, "warnings": warnings}
