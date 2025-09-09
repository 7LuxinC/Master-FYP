import re

SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "html", "css",
    "react", "node.js", "angular", "vue.js", "django", "flask", "spring", "ruby on rails",
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "linux", "windows server", "git", "jenkins", "ci/cd", "rest api", "graphql",
    "networking", "firewalls", "vmware", "data analysis", "big data", "hadoop",
    "spark", "etl", "sql server", "oracle", "mongodb", "nosql",
    "machine learning", "deep learning", "nlp", "computer vision", "ai",
    "qa", "testing", "automation testing", "manual testing", "selenium", "jira",
    "project management", "agile", "scrum", "kanban", "leadership", "teamwork",
    "communication", "problem solving", "critical thinking", "time management",
    "sales", "marketing", "seo", "content writing", "business analysis",
    "accounting", "finance", "budgeting", "customer service", "crm",
    "microsoft word", "ms word", "word", 
    "microsoft excel", "ms excel", "excel",
    "microsoft powerpoint", "ms powerpoint", "powerpoint",
    "microsoft outlook", "ms outlook", "outlook",
    "microsoft access", "ms access", "access",
    "google docs", "google sheets", "google slides", "google drive",
    "notion", "trello", "slack", "asana",
    "photoshop", "illustrator", "indesign", "figma", "sketch", "ux/ui design",
    "video editing", "after effects", "premiere pro", "coreldraw", "animation",
    "english", "spanish", "french", "german", "mandarin", "hindi",
    "research", "data visualization", "reporting", "presentation", "writing",
    "adaptability", "mentoring", "coaching", "training"
]


# Common education keywords
EDUCATION_KEYWORDS = [
    "bachelor", "b.sc", "b.a", "b.com", "b.tech", "b.eng", "bba",
    "bachelor of science", "bachelor of arts", "bachelor of commerce",
    "bachelor of technology", "bachelor of engineering", "bachelor of business administration",
    "master", "m.sc", "m.a", "m.com", "m.tech", "mba", "master of science",
    "master of arts", "master of commerce", "master of technology",
    "master of business administration",
    "phd", "doctor of philosophy", "d.phil", "doctorate",
    "associate", "associate degree", "diploma", "certificate", "certification",
    "vocational training", "professional course",
    "law degree", "llb", "llm", "medical degree", "md", "bds", "mds", "bachelors in nursing", "masters in nursing"
]


# Job titles for experience extraction
JOB_TITLES = [
    "developer", "software engineer", "web developer", "frontend developer", "backend developer",
    "fullstack developer", "data engineer", "data scientist", "machine learning engineer",
    "ai engineer", "nlp engineer", "devops engineer", "cloud engineer", "qa engineer",
    "system administrator", "network engineer", "security analyst", "it specialist",
    "database administrator", "product manager", "technical lead", "cto", "cio",
    "business analyst", "financial analyst", "accountant", "auditor", "consultant",
    "project manager", "operations manager", "sales manager", "marketing manager",
    "hr manager", "recruiter", "customer service manager", "strategist", "risk manager",
    "investment analyst", "portfolio manager",
    "graphic designer", "ux designer", "ui designer", "product designer", "visual designer",
    "animator", "video editor", "content writer", "copywriter", "creative director",
    "photographer", "illustrator",
    "doctor", "nurse", "pharmacist", "research scientist", "lab technician",
    "biologist", "chemist", "physicist", "clinical researcher",
    "administrator", "specialist", "coordinator", "trainer", "mentor", "lecturer", "teacher",
    "executive", "assistant", "intern", "technician", "supervisor"
]


def extract_info(text: str):
    info = {}

    # --- Contact info ---
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        info["email"] = email_match.group(0)

    phone_match = re.search(r'\+?\d[\d -]{8,}\d', text)
    if phone_match:
        info["phone"] = phone_match.group(0)

    # --- Skills Extraction ---
    found_skills = []
    for skill in SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            found_skills.append(skill)

    if found_skills:
        info["skills"] = list(set(found_skills))
    else:
        info["skills"] = "No skills found"

    # --- Education Extraction ---
    found_education = []
    for edu in EDUCATION_KEYWORDS:
        if re.search(rf"\b{re.escape(edu)}\b", text, re.IGNORECASE):
            found_education.append(edu.title())

    if found_education:
        info["education"] = list(set(found_education))
    else:
        info["education"] = "No education found"

    # --- Experience Extraction ---
    experience = {}

    # Years of experience
    years_match = re.findall(r'(\d+\+?\s+years?)', text, re.IGNORECASE)
    if years_match:
        experience["years"] = list(set([y.lower() for y in years_match]))

    date_ranges = re.findall(
        r'((?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{4})\s*[-–]\s*(?:\b(?:present|\d{4})))',
        text,
        re.IGNORECASE
    )
    if date_ranges:
        experience["date_ranges"] = date_ranges

    # Job titles
    found_titles = []
    for title in JOB_TITLES:
        if re.search(rf"\b{title}\b", text, re.IGNORECASE):
            found_titles.append(title.title())
    if found_titles:
        experience["job_titles"] = list(set(found_titles))

    if experience:
        info["experience"] = experience
    else:
        info["experience"] = "No experience found"

    return info
