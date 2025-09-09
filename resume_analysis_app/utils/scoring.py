import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- Load pre-trained model once ---
# NOTE: the app.py will cache this, but we keep a fallback here
model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

try:
    with open("notebooks/resume_analysis_app/models/saved_model/resume_embeddings_cpu.pkl", "rb") as f:
        resume_embeddings = pickle.load(f)
except:
    resume_embeddings = None


def encode_text(text: str, as_numpy=True):
    """
    Encode a single piece of text into a numpy embedding.
    """
    emb = model.encode([text], convert_to_tensor=True)
    return emb.cpu().numpy() if as_numpy else emb


def score_resume(resume_text: str, job_description: str) -> float:
    """
    Compute similarity score between ONE resume and ONE job description.
    Returns float between -1 and 1 (cosine similarity).
    """
    if not job_description or not resume_text:
        return 0.0

    resume_embedding = encode_text(resume_text)
    job_embedding = encode_text(job_description)

    sim = cosine_similarity(resume_embedding, job_embedding)[0][0]
    return round(float(sim), 4)


def rank_resumes(resumes: list, job_description: str) -> list:
    """
    Given a list of resumes and a job description,
    return the resumes ranked by similarity score.
    """
    if not job_description:
        return []

    # Precompute job description embedding once for efficiency
    job_embedding = encode_text(job_description)
    scored_resumes = []

    for resume in resumes:
        resume_embedding = encode_text(resume["text"])
        score = cosine_similarity(resume_embedding, job_embedding)[0][0]
        scored_resumes.append({
            "filename": resume["filename"],
            "score": round(float(score), 4)
        })

    ranked = sorted(scored_resumes, key=lambda x: x["score"], reverse=True)
    return ranked
