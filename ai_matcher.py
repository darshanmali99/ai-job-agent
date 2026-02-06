"""
AI-powered job-profile semantic matching layer.
Integrates with existing job_agent.py without breaking current logic.
"""

from sentence_transformers import SentenceTransformer, util
import logging

# ============================================
# CONFIGURATION
# ============================================
USER_PROFILE = """
Recent graduate seeking Data Analyst or Business Analyst internship opportunities.
Skills: Python, SQL, Excel, Power BI, Tableau, data visualization, statistical analysis.
Interests: Business analytics, data-driven insights, market research, dashboard creation.
Experience: Academic projects in data analysis, SQL databases, predictive modeling.
Looking for: Entry-level or internship roles in data/business analytics with learning opportunities.
Preferred: Remote work or positions in major Indian cities (Pune, Mumbai, Bangalore, Delhi, Hyderabad).
"""

MATCH_THRESHOLD = 0.45  # Lower threshold for entry-level jobs (they have shorter descriptions)
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

# ============================================
# AI MATCHER
# ============================================
class AIJobMatcher:
    def __init__(self, user_profile: str = USER_PROFILE):
        """Initialize Sentence-BERT matcher (one-time model load)"""
        print("🤖 Loading AI matcher model...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.user_embedding = self.model.encode(user_profile, convert_to_tensor=True)
        print("   ✅ AI matcher ready")
    
    def score_job(self, job: dict) -> float:
        """
        Compute semantic similarity between job and user profile.
        
        Args:
            job: Dict with 'title' and 'description' keys
        
        Returns:
            float: Cosine similarity [0.0, 1.0]
        """
        # Combine title (weighted 2x) + description + location + stipend
        title = job.get('title', '')
        desc = job.get('description', '')
        location = job.get('location', '')
        stipend = job.get('stipend', '')
        
        job_text = f"{title} {title} {desc} {location} {stipend}"
        
        if not job_text.strip():
            return 0.0
        
        try:
            job_embedding = self.model.encode(job_text, convert_to_tensor=True)
            similarity = util.cos_sim(self.user_embedding, job_embedding).item()
            return round(similarity, 4)
        except Exception as e:
            print(f"   ⚠️ AI scoring error: {e}")
            return 0.0
    
    def batch_score(self, jobs: list) -> list:
        """
        Score all jobs in batch.
        
        Args:
            jobs: List of job dicts
        
        Returns:
            Same list with 'ai_score' added to each job
        """
        if not jobs:
            return jobs
        
        print(f"🤖 AI scoring {len(jobs)} jobs...")
        
        scored_count = 0
        high_score_count = 0
        
        for job in jobs:
            job['ai_score'] = self.score_job(job)
            
            if job['ai_score'] > 0:
                scored_count += 1
            
            if job['ai_score'] >= MATCH_THRESHOLD:
                high_score_count += 1
        
        print(f"   ✅ Scored: {scored_count}/{len(jobs)} jobs")
        print(f"   ✅ High relevance (≥{MATCH_THRESHOLD}): {high_score_count} jobs")
        
        return jobs

# ============================================
# SINGLETON INSTANCE
# ============================================
_matcher_instance = None

def get_ai_matcher() -> AIJobMatcher:
    """Get or create AI matcher singleton"""
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = AIJobMatcher()
    return _matcher_instance
