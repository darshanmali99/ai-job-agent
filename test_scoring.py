"""
Quick diagnostic to test AI and Hybrid scoring
"""

# Test 1: Import AI matcher
try:
    from ai_matcher import get_ai_matcher
    print("✅ AI matcher import: SUCCESS")
    AI_ENABLED = True
except Exception as e:
    print(f"❌ AI matcher import: FAILED - {e}")
    AI_ENABLED = False

# Test 2: Import Hybrid scorer
try:
    from hybrid_scorer import add_hybrid_scores_to_jobs
    print("✅ Hybrid scorer import: SUCCESS")
    HYBRID_ENABLED = True
except Exception as e:
    print(f"❌ Hybrid scorer import: FAILED - {e}")
    HYBRID_ENABLED = False

# Test 3: Score test jobs
if AI_ENABLED and HYBRID_ENABLED:
    test_jobs = [
        {
            "title": "Data Analyst Intern (Excel, SQL, Power BI)",
            "description": "Entry-level opportunity",
            "location": "Remote"
        },
        {
            "title": "Business Analyst Intern",
            "description": "",
            "location": ""
        }
    ]
    
    print("\n" + "="*70)
    print("TESTING AI + HYBRID SCORING")
    print("="*70)
    
    # AI scoring
    matcher = get_ai_matcher()
    test_jobs = matcher.batch_score(test_jobs)
    
    # Hybrid scoring
    test_jobs = add_hybrid_scores_to_jobs(test_jobs)
    
    # Display results
    for i, job in enumerate(test_jobs, 1):
        print(f"\nJob {i}: {job['title']}")
        print(f"  AI Score:     {job.get('ai_score', 'MISSING')}")
        print(f"  Keyword Score: {job.get('keyword_score', 'MISSING')}")
        print(f"  Hybrid Score:  {job.get('hybrid_score', 'MISSING')}")
    
    print("\n" + "="*70)
    
    # Check if AI scores are 0
    ai_scores = [j.get('ai_score', 0) for j in test_jobs]
    if all(s == 0 for s in ai_scores):
        print("❌ PROBLEM: All AI scores are 0!")
        print("   This means AI matcher is returning 0 for all jobs.")
    else:
        print("✅ SUCCESS: AI scoring is working correctly!")
    
    print("="*70)
else:
    print("\n❌ Cannot test - imports failed")
