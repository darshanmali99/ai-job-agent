"""
Test Company Ranker
Verify tier classification and scoring logic
"""

from company_ranker import (
    normalize_company_name,
    get_company_tier,
    get_company_info,
    add_company_scores_to_jobs,
    calculate_final_rank,
    should_send_telegram_alert
)

# ============================================
# TEST CASES
# ============================================

test_companies = [
    # Tier 1 - Should score 1.0
    "Tata Consultancy Services Pvt Ltd",
    "Google India Private Limited",
    "Amazon Development Centre",
    "Flipkart Internet Pvt Ltd",
    "Accenture Solutions",
    "Deloitte Consulting",
    "Goldman Sachs Services",
    "Razorpay Software Pvt Ltd",
    
    # Tier 2 - Should score 0.85
    "Hexaware Technologies",
    "Unacademy",
    "BYJU'S",
    "OYO Rooms",
    "Naukri.com",
    
    # Tier 3 - Should score 0.4
    "Unknown Startup Pvt Ltd",
    "ABC Technologies",
    "XYZ Solutions",
    "Random Company",
    "LinkedIn",  # Test from your actual data
    "Internshala",  # Test from your actual data
]

print("="*70)
print("COMPANY RANKER TEST")
print("="*70)

for company in test_companies:
    info = get_company_info(company)
    
    print(f"\nCompany: {info['original_name']}")
    print(f"  Normalized: {info['normalized_name']}")
    print(f"  Tier: {info['tier']} - {info['tier_label']}")
    print(f"  Score: {info['company_score']}")
    print(f"  Telegram Alert: {'✅ YES' if info['telegram_alert'] else '❌ NO'}")

print("\n" + "="*70)
print("FULL JOB TEST")
print("="*70)

# Test full job workflow
test_jobs = [
    {
        "title": "Data Analyst Intern",
        "company": "Google India Pvt Ltd",
        "source": "LinkedIn",
        "ai_score": 0.85,
        "keyword_score": 1.0,
        "hybrid_score": 0.89
    },
    {
        "title": "Business Analyst",
        "company": "Random Startup Technologies",
        "source": "Internshala",
        "ai_score": 0.90,
        "keyword_score": 1.0,
        "hybrid_score": 0.93
    }
]

# Add company scores
test_jobs = add_company_scores_to_jobs(test_jobs)

for job in test_jobs:
    # Calculate final rank
    job['final_rank_score'] = calculate_final_rank(job)
    
    print(f"\nJob: {job['title']}")
    print(f"  Company: {job['company']}")
    print(f"  AI Score: {job['ai_score']}")
    print(f"  Hybrid Score: {job['hybrid_score']}")
    print(f"  Company Score: {job['company_score']}")
    print(f"  Final Rank: {job['final_rank_score']}")
    print(f"  Send Telegram: {'✅ YES' if should_send_telegram_alert(job) else '❌ NO'}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
