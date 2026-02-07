"""
Hybrid Match Score Module
Composes on top of existing AI score without modifying it.
Combines semantic AI score with keyword matching.
"""

import re
from typing import List, Tuple


# ============================================
# CONFIGURATION
# ============================================

# Skills to detect in job descriptions
REQUIRED_SKILLS = [
    "python", "sql", "excel", "power bi", "powerbi", "tableau", 
    "pandas", "numpy", "r programming", "statistics", "machine learning",
    "data visualization", "etl", "data warehouse", "dashboard",
    "jupyter", "matplotlib", "seaborn", "mysql", "postgresql"
]

# Weight configuration for hybrid score
AI_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3

# Default keyword score when no skills detected
DEFAULT_KEYWORD_SCORE = 0.5


# ============================================
# SKILL EXTRACTION
# ============================================

def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract mentioned required skills from job text.
    
    Args:
        text: Job description or resume text (lowercase)
    
    Returns:
        List of detected skills
    """
    text_lower = text.lower()
    detected = []
    
    for skill in REQUIRED_SKILLS:
        # Handle multi-word skills (e.g., "power bi")
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            detected.append(skill)
    
    return detected


# ============================================
# KEYWORD SCORE CALCULATION
# ============================================

def calculate_keyword_score(job_text: str, user_skills: List[str] = None) -> Tuple[float, dict]:
    """
    Calculate keyword matching score between job requirements and user skills.
    
    Args:
        job_text: Full job description text
        user_skills: List of user's skills (if None, uses default profile)
    
    Returns:
        Tuple of (keyword_score, metadata_dict)
        - keyword_score: float between 0 and 1
        - metadata: dict with 'required', 'matched', 'missing' skills
    """
    # Default user profile (can be customized)
    if user_skills is None:
        user_skills = [
            "python", "sql", "excel", "power bi", "tableau",
            "pandas", "data visualization", "statistics"
        ]
    
    # Extract required skills from job
    required_skills = extract_skills_from_text(job_text)
    
    # If no skills detected in job, return neutral score
    if not required_skills:
        return DEFAULT_KEYWORD_SCORE, {
            'required': [],
            'matched': [],
            'missing': [],
            'match_rate': DEFAULT_KEYWORD_SCORE
        }
    
    # Find matched skills
    user_skills_lower = [s.lower() for s in user_skills]
    matched_skills = [s for s in required_skills if s in user_skills_lower]
    missing_skills = [s for s in required_skills if s not in user_skills_lower]
    
    # Calculate score
    keyword_score = len(matched_skills) / len(required_skills)
    
    # Clamp between 0 and 1
    keyword_score = max(0.0, min(1.0, keyword_score))
    
    metadata = {
        'required': required_skills,
        'matched': matched_skills,
        'missing': missing_skills,
        'match_rate': keyword_score
    }
    
    return round(keyword_score, 4), metadata


# ============================================
# HYBRID SCORE CALCULATION
# ============================================

def calculate_hybrid_score(ai_score: float, keyword_score: float) -> float:
    """
    Combine AI semantic score with keyword matching score.
    
    Formula: Hybrid = (0.7 * AI_Score) + (0.3 * Keyword_Score)
    
    Args:
        ai_score: Existing AI semantic similarity score (0-1)
        keyword_score: Keyword matching score (0-1)
    
    Returns:
        float: Hybrid score between 0 and 1
    """
    # Ensure inputs are valid
    ai_score = max(0.0, min(1.0, ai_score))
    keyword_score = max(0.0, min(1.0, keyword_score))
    
    # Weighted combination
    hybrid_score = (AI_WEIGHT * ai_score) + (KEYWORD_WEIGHT * keyword_score)
    
    # Clamp final score
    hybrid_score = max(0.0, min(1.0, hybrid_score))
    
    return round(hybrid_score, 4)


# ============================================
# CONVENIENCE FUNCTION
# ============================================

def add_hybrid_score_to_job(job: dict) -> dict:
    """
    Add hybrid score to a job dict that already has 'ai_score'.
    This is the main integration point.
    
    Args:
        job: Job dict with at least 'ai_score', 'title', 'description'
    
    Returns:
        Same job dict with added fields:
        - 'keyword_score': float
        - 'hybrid_score': float
        - 'skill_match': dict with match metadata
    """
    # Get existing AI score
    ai_score = job.get('ai_score', 0.0)
    
    # If AI score is None or missing, set to 0
    if ai_score is None:
        ai_score = 0.0
    
    # Build job text for keyword extraction
    job_text = f"{job.get('title', '')} {job.get('description', '')}"
    
    # Calculate keyword score
    keyword_score, skill_metadata = calculate_keyword_score(job_text)
    
    # Calculate hybrid score
    hybrid_score = calculate_hybrid_score(ai_score, keyword_score)
    
    # Add to job dict (NON-DESTRUCTIVE)
    job['keyword_score'] = keyword_score
    job['hybrid_score'] = hybrid_score
    job['skill_match'] = skill_metadata
    
    return job


# ============================================
# BATCH PROCESSING
# ============================================

def add_hybrid_scores_to_jobs(jobs: List[dict]) -> List[dict]:
    """
    Add hybrid scores to a list of jobs.
    Safe to call even if jobs don't have AI scores yet.
    
    Args:
        jobs: List of job dicts
    
    Returns:
        Same list with hybrid scores added
    """
    for job in jobs:
        add_hybrid_score_to_job(job)
    
    return jobs
