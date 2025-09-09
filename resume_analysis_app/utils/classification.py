import joblib
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import os

# fixed model dir
model_dir = os.path.join("models", "transformer_model")

# load classifier
clf = joblib.load(os.path.join(model_dir, "classifier.pkl"))

# load BERT encoder + tokenizer
tokenizer = BertTokenizer.from_pretrained(model_dir)
bert_model = BertModel.from_pretrained(model_dir)

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
