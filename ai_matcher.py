"""
AI Score Explainer - Debug tool to understand why jobs get certain scores
"""

from ai_matcher import get_ai_matcher

def explain_score(job: dict):
    """
    Explain in detail why a job received its AI score.
    Useful for tuning the scoring algorithm.
    """
    matcher = get_ai_matcher()
    
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    location = job.get("location", "").lower()
    
    print("=" * 70)
    print(f"JOB: {job.get('title', 'Unknown')}")
    print("=" * 70)
    
    # Show inputs
    print(f"\nTitle: {title}")
    print(f"Description: {description}")
    print(f"Location: {location}")
    
    # Score breakdown
    print("\n" + "-" * 70)
    print("SCORING BREAKDOWN:")
    print("-" * 70)
    
    score = 0.0
    
    # Title analysis
    title_text = f"{title} {title} {title} {title}"
    full_text = f"{title_text} {description} {location}"
    
    # High priority in title
    title_high = [skill for skill in matcher.high_priority_skills if skill in title]
    title_high_score = min(len(title_high) * 0.20, 0.80)
    score += title_high_score
    print(f"\n1. High Priority Skills in Title (+0.20 each, max 0.80):")
    if title_high:
        for skill in title_high:
            print(f"   ✓ {skill}")
        print(f"   → Score: +{title_high_score:.2f}")
    else:
        print(f"   (none found)")
        print(f"   → Score: +0.00")
    
    # High priority in full text
    text_high = [skill for skill in matcher.high_priority_skills if skill in full_text]
    text_high_score = min(len(text_high) * 0.10, 0.40)
    score += text_high_score
    print(f"\n2. High Priority Skills in Full Text (+0.10 each, max 0.40):")
    if text_high:
        for skill in text_high:
            print(f"   ✓ {skill}")
        print(f"   → Score: +{text_high_score:.2f}")
    else:
        print(f"   (none found)")
        print(f"   → Score: +0.00")
    
    # Medium priority
    medium = [skill for skill in matcher.medium_priority_skills if skill in full_text]
    medium_score = min(len(medium) * 0.08, 0.30)
    score += medium_score
    print(f"\n3. Medium Priority Skills (+0.08 each, max 0.30):")
    if medium:
        for skill in medium:
            print(f"   ✓ {skill}")
        print(f"   → Score: +{medium_score:.2f}")
    else:
        print(f"   (none found)")
        print(f"   → Score: +0.00")
    
    # Positive keywords
    positive = [kw for kw in matcher.positive_keywords if kw in full_text]
    positive_score = min(len(positive) * 0.05, 0.15)
    score += positive_score
    print(f"\n4. Positive Keywords (+0.05 each, max 0.15):")
    if positive:
        for kw in positive:
            print(f"   ✓ {kw}")
        print(f"   → Score: +{positive_score:.2f}")
    else:
        print(f"   (none found)")
        print(f"   → Score: +0.00")
    
    # Bonus
    bonus_keywords = ["intern", "internship", "entry level", "junior"]
    has_bonus = any(kw in title for kw in bonus_keywords)
    bonus_score = 0.10 if has_bonus else 0.0
    score += bonus_score
    print(f"\n5. Entry-Level Bonus (+0.10):")
    if has_bonus:
        matched = [kw for kw in bonus_keywords if kw in title]
        print(f"   ✓ Found: {', '.join(matched)}")
        print(f"   → Score: +{bonus_score:.2f}")
    else:
        print(f"   (not entry-level)")
        print(f"   → Score: +0.00")
    
    # Final score
    final_score = round(min(score, 1.0), 4)
    
    print("\n" + "=" * 70)
    print(f"FINAL AI SCORE: {final_score} ({int(final_score*100)}%)")
    print("=" * 70)
    
    # Interpretation
    if final_score >= 0.70:
        print("\n🎯 EXCELLENT MATCH - Highly relevant to your profile")
    elif final_score >= 0.50:
        print("\n✅ GOOD MATCH - Relevant opportunity worth applying to")
    elif final_score > 0:
        print("\n⚡ SCORED - Some relevance, review carefully")
    else:
        print("\n❌ NO MATCH - Not relevant to your profile")
    
    print()


if __name__ == "__main__":
    # Test with sample jobs
    test_jobs = [
        {
            "title": "Junior Data Analyst",
            "description": "",
            "location": ""
        },
        {
            "title": "Data Analyst Intern (Excel, SQL, Power BI)",
            "description": "Entry-level opportunity",
            "location": "Remote"
        },
        {
            "title": "Business Analyst Intern",
            "description": "Remote opportunity for entry-level analyst",
            "location": "Remote"
        }
    ]
    
    for job in test_jobs:
        explain_score(job)
        print("\n" * 2)
