import streamlit as st
import pandas as pd

from utils.extract_text import extract_text
from utils.info_extraction import extract_info
from utils.classification import classify_resume
from utils.scoring import score_resume

# --- Streamlit App ---
st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("🗃️ Resume Analysis Tool using NLP and ML")


# -------------------------------
# Cache helpers
# -------------------------------
@st.cache_data
def cached_extract_text(file):
    return extract_text(file)

@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

# load model once
model = load_model()


# -------------------------------
# File Upload
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload your resume(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True
)

if uploaded_files:
    # Store extracted texts in session_state so they persist across reruns
    if "resume_texts" not in st.session_state:
        st.session_state.resume_texts = {}

    for resume_file in uploaded_files:
        if resume_file.name not in st.session_state.resume_texts:
            st.session_state.resume_texts[resume_file.name] = cached_extract_text(resume_file)

    # Take only the most recent uploaded file for display
    latest_file = uploaded_files[-1]
    st.subheader(f"📜 Resume: {latest_file.name}")

    # Extracted resume text
    text = st.session_state.resume_texts[latest_file.name]
    st.text_area("Extracted Text", text, height=250)


    # -------------------------------
    # Extract structured info
    # -------------------------------
    info = extract_info(text)
    st.subheader("🔍 Extracted Information")

    if info:
        if "name" in info:
            st.write(f"**Name:** {info['name']}")
        if "email" in info:
            st.write(f"**Email:** {info['email']}")
        if "phone" in info:
            st.write(f"**Phone:** {info['phone']}")
        if "skills" in info:
            st.write(f"**Skills:** {', '.join(info['skills']) if isinstance(info['skills'], list) else info['skills']}")
        if "education" in info:
            st.write(f"**Education:** {', '.join(info['education']) if isinstance(info['education'], list) else info['education']}")
        if "experience" in info:
            if isinstance(info["experience"], dict):
                exp = info["experience"]
                if "years" in exp:
                    st.write(f"**Years of Experience:** {', '.join(exp['years'])}")
                if "date_ranges" in exp:
                    st.write(f"**Date Ranges:** {', '.join(exp['date_ranges'])}")
                if "job_titles" in exp:
                    st.write(f"**Job Titles:** {', '.join(exp['job_titles'])}")
            else:
                st.write(f"**Experience:** {info['experience']}")
    else:
        st.write("No information extracted.")


    # -------------------------------
    # Classification
    # -------------------------------
    st.subheader("🧾 Resume Classification")
    try:
        category = classify_resume(text)
        st.success(f"Predicted Job Category: {category}")
    except Exception as e:
        st.error(f"Error classifying resume: {e}")


    # -------------------------------
    # Resume Score Section
    # -------------------------------
    st.header("⭐ Resume Score Based on Job Description")
    job_description = st.text_area("Enter Job Description", height=150)

    if job_description.strip() == "":
        st.info("Enter a job description to get resume score.")

    if st.button("Get Resume Score"):
        if job_description.strip() == "":
            st.warning("Please enter a job description to get resume score.")
        else:
            scored_resumes = []

            # Compute scores using cached resume text
            for resume_file in uploaded_files:
                resume_text = st.session_state.resume_texts[resume_file.name]
                score = score_resume(resume_text, job_description)
                score_scaled = (score + 1) / 2  # Scale -1..1 → 0..1
                scored_resumes.append({"Resume": resume_file.name, "Score": round(score_scaled, 2)})

            # Get the score of the latest uploaded resume
            latest_resume_entry = next(
                (r for r in scored_resumes if r["Resume"] == latest_file.name), None
            )

            if latest_resume_entry:
                latest_score = latest_resume_entry["Score"]

                st.subheader(f"📄 Resume Review: {latest_file.name}")
                st.progress(latest_score)
                st.markdown(
                    f"<h3 style='text-align: center; color: #1f77b4;'>Score: {latest_score:.2f}</h3>",
                    unsafe_allow_html=True
                )

                # Evaluation
                if latest_score >= 0.76:
                    evaluation = "Excellent ⭐⭐⭐⭐"
                    color = "#28a745"
                elif latest_score >= 0.51:
                    evaluation = "Good ⭐⭐⭐"
                    color = "#17a2b8"
                elif latest_score >= 0.26:
                    evaluation = "Fair ⭐⭐"
                    color = "#ffc107"
                else:
                    evaluation = "Poor ⭐"
                    color = "#dc3545"

                st.markdown(
                    f"<h4 style='text-align: center; color: {color};'>Evaluation: {evaluation}</h4>",
                    unsafe_allow_html=True
                )

            # Ranking
            ranked_resumes = sorted(scored_resumes, key=lambda x: x["Score"], reverse=True)
            st.subheader("📊 Resume Ranking")
            st.table(ranked_resumes)
