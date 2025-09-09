#use joblib to load the model
import joblib
import torch
from transformers import BertTokenizer, BertModel
import numpy as np

# load the model from huggingface hub since the model cannot upload to github
model_repo = "3Ellie/resume-transformer"
# Load classifier directly from Hugging Face
from huggingface_hub import hf_hub_download

clf_path = hf_hub_download(repo_id=model_repo, filename="classifier.pkl")
clf = joblib.load(clf_path)

# Load BERT tokenizer and model directly from Hugging Face
tokenizer = BertTokenizer.from_pretrained(model_repo)
bert_model = BertModel.from_pretrained(model_repo)

def get_bert_embedding(text: str) -> np.ndarray:
    """
    Extract BERT [CLS] token embedding for given text
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # CLS token embedding
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embedding

def classify_resume(text: str) -> str:
    """
    Classify resume text into a job category
    """
    embedding = get_bert_embedding(text)
    prediction = clf.predict(embedding)[0]
    return prediction

sample_resume = "Experienced Python developer with knowledge of ML and NLP."
print("Predicted Category:", classify_resume(sample_resume))
