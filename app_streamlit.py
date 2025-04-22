import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professors (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            mobile TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password, mobile):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO professors (username, password, mobile) VALUES (?, ?, ?)",
                       (username, password, mobile))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professors WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Initialize DB
init_db()

import sqlite3

# Create DB table if not exists
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS professors (
                        username TEXT PRIMARY KEY,
                        password TEXT)""")
    conn.commit()
    conn.close()

def register_user(username, password, mobile):  
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO professors (username, password, mobile) VALUES (?, ?, ?)",
                       (username, password, mobile))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# Validate login
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professors WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Initialize DB
init_db()

import streamlit as st
import PyPDF2
import pytesseract
from PIL import Image
from validation_utils import validate_paper  

# Dummy credentials for login
USER_CREDENTIALS = {"professor": "password123"}

# Set Streamlit page config
st.set_page_config(page_title="AI-Powered Question Paper Validator", layout="wide")

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---- LOGIN SECTION ---- #
if not st.session_state.logged_in:
    st.title("🔐 Professor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):

            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()  # Refresh the page to enter upload section
        else:
            st.error("❌ Invalid username or password!")
with st.expander("📋 Register as Professor"):
    new_user = st.text_input("👤 New Username")
    new_pass = st.text_input("🔒 New Password", type="password")
    new_mobile = st.text_input("📞 Mobile Number")

    if st.button("Register"):
        if register_user(new_user, new_pass, new_mobile):
            st.success("✅ Registered successfully! Please login.")
        else:
            st.warning("⚠ Username already exists. Try a different one.")


# ---- UPLOAD & VALIDATION SECTION ---- #
if st.session_state.logged_in:
    st.title("AI-Powered Question Paper Validator")

    # Upload a file
    uploaded_file = st.file_uploader("Upload a question paper (PDF, TXT, PNG, JPG)", type=["pdf", "txt", "png", "jpg"])

    extracted_text = ""

    # Extract text if a file is uploaded
    if uploaded_file:
        file_type = uploaded_file.type
        st.write(f"**Uploaded File:** {uploaded_file.name}")

        if file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        elif file_type == "text/plain":
            extracted_text = uploaded_file.read().decode("utf-8")
        elif file_type in ["image/png", "image/jpeg"]:
            image = Image.open(uploaded_file)
            extracted_text = pytesseract.image_to_string(image)
        else:
            st.error("❌ Unsupported file format!")

    # Manual text input option
    st.subheader("📌 Enter/Paste Question Paper:")
    content = st.text_area("Paste Question Paper Here:", extracted_text, height=300)

    # ✅ Corrected Validate Button Logic
    if st.button("Validate"):
        #st.write("🔍 Debug: Validate button clicked!")  # Debugging step
        validation_results = validate_paper(content)  # Run validation
        #st.write(f"📌 Debug: Validation Results = {validation_results}")  # Check output

        if validation_results:
            st.subheader("🔍 Validation Results")

            # Show Errors
            if validation_results.get("errors"):
                st.error("❌ **Errors Found:**")
                for error in validation_results["errors"]:
                    st.markdown(f"- ❌ **{error}**")

            # Show Warnings
            if validation_results.get("warnings"):
                st.warning("⚠ **Warnings:**")
                for warning in validation_results["warnings"]:
                    st.markdown(f"- ⚠ {warning}")

            # If no errors, show success message
            if not validation_results.get("errors"):
                st.success("✅ No major issues found! The paper is valid.")

            # Suggested Next Steps
            st.info("💡 **Next Steps:**\n- Please review the errors and update the question paper.\n- If necessary, re-upload and validate again.")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()  # Refresh page to go back to login
