import re
import nltk
import spacy
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# ---------- CLEANING ----------
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\r", "").replace("\n", " ")
    text = text.encode("ascii", errors="ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text)
    return text.lower()

def clean_skills_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    tokens = text.lower().split()
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

# ---------- EXTRACTION ----------
def extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else None

def extract_phone(text: str) -> str:
    match = re.search(r"\+?\d[\d\s\-\(\)]{7,}\d", text)
    return match.group(0) if match else None

def extract_education(text: str) -> str:
    patterns = ["bachelor", "master", "phd", "b\\.sc", "m\\.sc", "mba"]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return p
    return None

def extract_skills(text: str) -> list:
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return list(set(tokens))

def extract_experience(text: str) -> str:
    match = re.search(r"(\\d+)\\s+(years?|months?)", text)
    return match.group(0) if match else None

def extract_resume_info(text: str) -> dict:
    text = clean_text(text)
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
    }

# ---------- CLASSIFICATION (demostration exp3 works) ----------
def classify_resume(text: str) -> str:
    # load transformer model from exp3 notebook
    # 
    return "Data Scientist"

# ---------- SCORING + JOB MATCHING (demostration exp5 work) ----------
def score_and_match_resume(text: str):
    # TODO: implement from exp5 notebook
    score = 85
    jobs = ["Machine Learning Engineer", "Data Analyst"]
    return score, jobs
