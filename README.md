#  Interactive Resume Analysis using NLP and Machine Learning
- This repository contains all the experiments, datasets and Streamlit app development work carried out as part of a dissertation project. The project demostrates information extraction, classification, and resume evaluation using Natural Language Processing(NLP) and Machine Learning(ML) methods.
- The web app applies the trained models and techniques used in the experiment to provide a pratical demostration where users can upload resumes for evaluation and hiring teams also can check if paritcular candidate fit the job they posted.
---

## About the Project
The primary goal of this research is to explore different NLP-based methods for:  
1. Resume information extraction 
2. Resume classification 
3. Resume scoring and evaluation

The app integrates the best-performing techniques identified during dissertation experiments:

-  **Information Extraction** :  Rule-based techniques to extract key details from resumes.  
-  **Classification** :  Implemented with BERT + Logistic Regression (LR) for accurate resume categorization.  
-  **Scoring & Ranking**:  Uses DistilBERT embeddings and cosine similarity to evaluate and rank resumes.  

The app combines these approaches to provide an interactive demo of automated resume analysis.

---

##  Features

- Upload resumes in PDF, DOCX, or TXT format  
- Extract resume content into txt file
- Perform information extraction to identify key details  
- Classify resumes by job area/domain using BERT + LR 
- Provide resume scoring & ranking based on a user-provided job description (DistilBERT + cosine similarity)  


---

## Datasets Used

- **Experiments 1-3**: [Resume Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)  
- **Experiments 4-5**: [Resume and Job Description Dataset](https://www.kaggle.com/datasets/pranavvenugo/resume-and-job-description)  

---

## Classification Model 
- The model trained in the experiment is saved on Hugging Face at this repositoryhttps://huggingface.co/3Ellie/resume-transformer/tree/main. The application retrieves the model from Hugging Face and uses it to perform classification.

---

## How to Run

1. **Download** the project and navigate to its directory.  
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
3. **Install dependencies:**  
   ```bash
   streamlit run app.py
4. **Open in your Browser:**
   - Local: http://localhost:8501/ 
   - Online demo: https://resume-analysis-demo.streamlit.app/

