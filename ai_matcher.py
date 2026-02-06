"""
AI-powered job-profile semantic matching layer.
Lightweight keyword-based approach - no ML dependencies required.
Works on any Python 3.8+ environment, CPU-only.
"""

from typing import List, Dict


class AIJobMatcher:
    """
    Keyword-based job relevance scorer.
    Fallback implementation that works without sentence-transformers.
    """
    
    def __init__(self):
        """Initialize with user skill profile"""
        print("AI matcher initializing...")
        
        # User profile as weighted keywords
        self.high_priority_skills = [
            "data analyst", "data analysis", "business analyst",
            "analytics", "sql", "python", "excel", "power bi", "tableau"
        ]
        
        self.medium_priority_skills = [
            "intern", "internship", "entry level", "junior", "fresher",
            "data visualization", "reporting", "dashboard", "bi"
        ]
        
        self.positive_keywords = [
            "remote", "work from home", "paid", "stipend", "training",
            "statistics", "data science", "machine learning", "pandas"
        ]
        
        print("   AI matcher ready")
    
    def score_job(self, job: Dict) -> float:
        """
        Compute relevance score for a single job.
        
        Args:
            job: Dict with 'title' and 'description' keys
        
        Returns:
            float: Relevance score [0.0, 1.0]
        """
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        location = job.get("location", "").lower()
        
        # Combine all text (title weighted 2x)
        text = f"{title} {title} {description} {location}"
        
        if not text.strip():
            return 0.0
        
        score = 0.0
        
        # High priority matches (0.15 each, max 0.60)
        high_matches = sum(1 for skill in self.high_priority_skills if skill in text)
        score += min(high_matches * 0.15, 0.60)
        
        # Medium priority matches (0.10 each, max 0.30)
        medium_matches = sum(1 for skill in self.medium_priority_skills if skill in text)
        score += min(medium_matches * 0.10, 0.30)
        
        # Positive keywords (0.05 each, max 0.20)
        positive_matches = sum(1 for kw in self.positive_keywords if kw in text)
        score += min(positive_matches * 0.05, 0.20)
        
        # Normalize to [0.0, 1.0]
        return round(min(score, 1.0), 4)
    
    def batch_score(self, jobs: List[Dict]) -> List[Dict]:
        """
        Score multiple jobs efficiently.
        
        Args:
            jobs: List of job dicts
        
        Returns:
            Same list with 'ai_score' added to each job
        """
        if not jobs:
            return jobs
        
        print(f"AI scoring {len(jobs)} jobs...")
        
        scored_count = 0
        high_score_count = 0
        total_score = 0.0
        
        for job in jobs:
            score = self.score_job(job)
            job["ai_score"] = score
            
            if score > 0:
                scored_count += 1
                total_score += score
            
            if score >= 0.50:
                high_score_count += 1
        
        avg_score = total_score / scored_count if scored_count > 0 else 0.0
        
        print(f"   Scored: {scored_count}/{len(jobs)} jobs")
        print(f"   High relevance (>=0.50): {high_score_count} jobs")
        print(f"   Average score: {avg_score:.3f}")
        
        return jobs


# ============================================
# SINGLETON INSTANCE
# ============================================
_matcher_instance = None


def get_ai_matcher() -> AIJobMatcher:
    """
    Get or create AI matcher singleton.
    Used by job_agent.py
    """
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = AIJobMatcher()
    return _matcher_instance
