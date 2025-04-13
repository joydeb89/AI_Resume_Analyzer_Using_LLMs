from backend.model import get_embedding_model
from backend.utils import extract_keywords
from sentence_transformers.util import pytorch_cos_sim  # ✅ Correct import

import numpy as np

# Load transformer model (once)
model = get_embedding_model()

def analyze_resume_job_match(resume_text: str, jd_text: str) -> dict:
    """
    Compares resume with job description and returns analysis.
    """
    # Step 1: Compute embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)

    # Step 2: Compute cosine similarity using pytorch_cos_sim directly
    similarity_score = pytorch_cos_sim(resume_embedding, jd_embedding).item()
    match_percentage = round(similarity_score * 100, 2)

    # Step 3: Extract keywords (skills) from both texts
    resume_skills = extract_keywords(resume_text)
    jd_skills = extract_keywords(jd_text)

    # Step 4: Identify missing skills
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    return {
        "match_score": match_percentage,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "recommendations": generate_recommendations(missing_skills)
    }

def generate_recommendations(missing_skills: list) -> list:
    """
    Provide recommendations based on missing skills.
    """
    return [f"Consider adding or learning: {skill}" for skill in missing_skills]
#------------------------------------------------------------------
from backend.model import get_embedding_model
from backend.utils import extract_keywords
from sentence_transformers.util import pytorch_cos_sim

# Load model once
model = get_embedding_model()

def analyze_resume_job_match(resume_text: str, jd_text: str) -> dict:
    # Embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)

    # Similarity score
    similarity_score = pytorch_cos_sim(resume_embedding, jd_embedding).item()
    match_percentage = round(similarity_score * 100, 2)

    # Keyword extraction
    resume_skills = extract_keywords(resume_text)
    jd_skills = extract_keywords(jd_text)
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    return {
        "match_score": match_percentage,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing_skills,
        "recommendations": generate_recommendations(missing_skills)
    }

def generate_recommendations(missing_skills: list) -> list:
    return [f"Consider learning: {skill}" for skill in missing_skills]
