import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Load pre-trained model once ---
model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

try:
    with open("notebooks/resume_analysis_app/models/saved_model/resume_embeddings_cpu.pkl", "rb") as f:
        resume_embeddings = pickle.load(f)
except:
    resume_embeddings = None

def score_resume(resume_text: str, job_description: str) -> float:
    """
    Compute similarity score between ONE resume and ONE job description.
    Returns float between -1 and 1 (cosine similarity).
    """
    if not job_description or not resume_text:
        return 0.0

    # Encode texts
    resume_embedding = model.encode([resume_text], convert_to_tensor=True)
    job_embedding = model.encode([job_description], convert_to_tensor=True)

    # Compute cosine similarity
    sim = cosine_similarity(resume_embedding.cpu(), job_embedding.cpu())[0][0]
    
    return round(float(sim), 4)

def rank_resumes(resumes: list, job_description: str) -> list:
    """
    Given a list of resumes and a job description,
    return the resumes ranked by similarity score.
    """
    scored_resumes = []
    for resume in resumes:
        score = score_resume(resume["text"], job_description)
        scored_resumes.append({"filename": resume["filename"], "score": score})
    
    ranked = sorted(scored_resumes, key=lambda x: x["score"], reverse=True)
    return ranked
