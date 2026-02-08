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
        
        # Enhanced: Give even more weight to title (4x vs 1x for desc)
        title_text = f"{title} {title} {title} {title}"
        full_text = f"{title_text} {description} {location}"
        
        if not title.strip():
            return 0.0
        
        score = 0.0
        
        # ENHANCED SCORING SYSTEM
        
        # High priority skills in title (0.20 each, max 0.80)
        title_high_matches = sum(1 for skill in self.high_priority_skills if skill in title)
        score += min(title_high_matches * 0.20, 0.80)
        
        # High priority in full text (0.10 each, max 0.40)
        text_high_matches = sum(1 for skill in self.high_priority_skills if skill in full_text)
        score += min(text_high_matches * 0.10, 0.40)
        
        # Medium priority matches (0.08 each, max 0.30)
        medium_matches = sum(1 for skill in self.medium_priority_skills if skill in full_text)
        score += min(medium_matches * 0.08, 0.30)
        
        # Positive keywords (0.05 each, max 0.15)
        positive_matches = sum(1 for kw in self.positive_keywords if kw in full_text)
        score += min(positive_matches * 0.05, 0.15)
        
        # BONUS: If it's explicitly an internship/entry-level role
        if any(kw in title for kw in ["intern", "internship", "entry level", "junior"]):
            score += 0.10
        
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
