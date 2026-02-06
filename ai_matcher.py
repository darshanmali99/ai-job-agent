"""
Diagnostic script to test AI scoring with sample LinkedIn job data.
Run this to verify AI matcher is working correctly.
"""

# Sample job data (like what LinkedIn scraper returns)
sample_jobs = [
    {
        "title": "Data Analyst Intern (Excel, SQL, Power BI)",
        "link": "https://linkedin.com/job/123",
        "source": "LinkedIn",
        "description": "",  # LinkedIn often has empty description
        "location": "",
        "stipend": "",
        "easy_apply": False
    },
    {
        "title": "Business Analyst Intern",
        "link": "https://linkedin.com/job/456",
        "source": "LinkedIn",
        "description": "Remote opportunity for entry-level analyst",
        "location": "Remote",
        "stipend": "",
        "easy_apply": False
    }
]

print("=" * 70)
print("🧪 AI MATCHER DIAGNOSTIC TEST")
print("=" * 70)

# Test 1: Import check
print("\n1️⃣ Testing AI matcher import...")
try:
    from ai_matcher import get_ai_matcher
    print("   ✅ Import successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

# Test 2: Model loading
print("\n2️⃣ Testing model loading...")
try:
    matcher = get_ai_matcher()
    print("   ✅ Model loaded successfully")
except Exception as e:
    print(f"   ❌ Model loading failed: {e}")
    exit(1)

# Test 3: Scoring jobs
print("\n3️⃣ Testing job scoring...")
try:
    scored_jobs = matcher.batch_score(sample_jobs)
    print("   ✅ Scoring completed")
    
    print("\n📊 Results:")
    for job in scored_jobs:
        score = job.get('ai_score', 0)
        emoji = "🎯" if score >= 0.70 else "✅" if score >= 0.50 else "⚡" if score > 0 else "❌"
        print(f"   {emoji} {job['title'][:50]}")
        print(f"      Score: {score} | Description: '{job['description'][:50]}'")
        print()
    
except Exception as e:
    print(f"   ❌ Scoring failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Check for zero scores
print("\n4️⃣ Analyzing score distribution...")
scores = [j.get('ai_score', 0) for j in scored_jobs]
zero_scores = sum(1 for s in scores if s == 0)
low_scores = sum(1 for s in scores if 0 < s < 0.30)
good_scores = sum(1 for s in scores if s >= 0.50)

print(f"   Total jobs: {len(scores)}")
print(f"   Zero scores: {zero_scores}")
print(f"   Low scores (0-0.30): {low_scores}")
print(f"   Good scores (0.50+): {good_scores}")

if zero_scores == len(scores):
    print("\n   ⚠️ WARNING: All scores are zero!")
    print("   ⚠️ This means job descriptions are empty or too short")
    print("   ⚠️ LinkedIn scraper may need improvement")
else:
    print("\n   ✅ AI scoring is working correctly!")

print("\n" + "=" * 70)
print("🎯 DIAGNOSTIC COMPLETE")
print("=" * 70)
