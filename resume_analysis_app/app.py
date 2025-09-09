import streamlit as st
import pandas as pd

from utils.extract_text import extract_text
from utils.info_extraction import extract_info
from utils.classification import classify_resume
from utils.scoring import score_resume

# --- Streamlit App ---
st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄Resume Analyser App")

# Upload one or multiple resumes
uploaded_files = st.file_uploader(
    "Upload your resume(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True
)

if uploaded_files:
    resumes_texts = []

    for uploaded_file in uploaded_files:
        st.subheader(f"📄 Resume: {uploaded_file.name}")

        # Extract resume text
        text = extract_text(uploaded_file)
        resumes_texts.append({"filename": uploaded_file.name, "text": text})

        st.text_area("Extracted Text", text, height=250)

        # Extract structured information
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

        # Classification
        category = classify_resume(text)
        st.subheader("🧾 Resume Classification")
        st.success(f"Predicted Job Category: {category}")

    # --- Resume Score Section ---
    st.header("⭐ Resume Score Based on Job Description")
    job_description = st.text_area("Enter Job Description", height=150)

    # Show info if job description is empty
    if job_description.strip() == "":
        st.info("Enter a job description to get resume scores.")

    # Button to trigger scoring
    if st.button("Get Resume Score"):
        if job_description.strip() == "":
            st.warning("Please enter a job description to get resume scores.")
        else:
            scored_resumes = []

            # Compute scores for all resumes (for ranking)
            for resume in resumes_texts:
                score = score_resume(resume["text"], job_description)
                score_scaled = (score + 1) / 2  # Scale 0-1 for progress bar
                scored_resumes.append({"Resume": resume["filename"], "Score": round(score_scaled, 2)})

            # Show progress bar and decorated score for most recent resume
            latest_resume = resumes_texts[-1]
            latest_score = scored_resumes[-1]["Score"]

            st.subheader(f"📄 Resume Review: {latest_resume['filename']}")
            st.progress(latest_score)

            # Decorated numerical score
            st.markdown(
                f"<h3 style='text-align: center; color: #1f77b4;'>Score: {latest_score:.2f}</h3>",
                unsafe_allow_html=True
            )

            # Evaluation (qualitative assessment with 4 levels)
            if latest_score >= 0.76:
                evaluation = "Excellent ⭐⭐⭐⭐"
                color = "#28a745"  # green
            elif latest_score >= 0.51:
                evaluation = "Good ⭐⭐⭐"
                color = "#17a2b8"  # blue
            elif latest_score >= 0.26:
                evaluation = "Fair ⭐⭐"
                color = "#ffc107"  # yellow
            else:
                evaluation = "Poor ⭐"
                color = "#dc3545"  # red

            st.markdown(
                f"<h4 style='text-align: center; color: {color};'>Evaluation: {evaluation}</h4>",
                unsafe_allow_html=True
            )

            # Display ranking table for all resumes
            ranked_resumes = sorted(scored_resumes, key=lambda x: x["Score"], reverse=True)
            st.subheader("🏆 Resume Ranking")
            st.table(ranked_resumes)
