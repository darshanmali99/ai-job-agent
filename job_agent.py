import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# ============ CONFIG ============
TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")
TELEGRAM_API = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"

# ============ TELEGRAM ============
def send_telegram(msg):
    """Send message to Telegram with error handling"""
    try:
        response = requests.post(
            TELEGRAM_API,
            data={"chat_id": 1474889968, "text": msg[:4000], "parse_mode": "HTML"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Telegram sent")
        else:
            print(f"❌ Telegram failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# ============ JOB SOURCES ============

def indeed_jobs():
    """Indeed RSS - Most reliable source"""
    try:
        url = "https://in.indeed.com/rss?q=data+analyst+intern&l=India"
        print(f"🔍 Fetching Indeed: {url}")
        r = requests.get(url, timeout=15)
        print(f"   Status: {r.status_code}")
        soup = BeautifulSoup(r.content, "xml")
        jobs = []
        items = soup.find_all("item")
        print(f"   Found {len(items)} raw items")
        
        for item in items[:10]:
            title = item.title.text.strip()
            link = item.link.text.strip()
            jobs.append({"title": title, "link": link, "source": "Indeed"})
            print(f"   - {title[:50]}...")
        
        print(f"✅ Indeed: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Indeed failed: {e}")
        return []

def internshala_jobs():
    """Internshala - Multiple selector strategies"""
    try:
        url = "https://internshala.com/internships/data-analyst-internship/"
        print(f"🔍 Fetching Internshala: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        print(f"   Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # Strategy 1: Look for internship cards
        containers = soup.select(".internship_meta")
        print(f"   Strategy 1 (.internship_meta): {len(containers)} found")
        
        if not containers:
            # Strategy 2: Look for individual internship divs
            containers = soup.select(".individual_internship")
            print(f"   Strategy 2 (.individual_internship): {len(containers)} found")
        
        if not containers:
            # Strategy 3: Any div with internship in class
            containers = soup.find_all("div", class_=lambda x: x and "internship" in x.lower())
            print(f"   Strategy 3 (div with 'internship'): {len(containers)} found")
        
        for container in containers[:10]:
            # Try multiple title selectors
            title_elem = (
                container.select_one(".job-internship-name") or
                container.select_one(".profile h3") or
                container.select_one("h3") or
                container.select_one("h4") or
                container.find("a")
            )
            
            if not title_elem:
                continue
                
            title = title_elem.get_text(strip=True)
            
            # Try to find link
            link_elem = container.select_one("a[href*='/internship/detail/']")
            if not link_elem:
                link_elem = container.find("a", href=True)
            
            if link_elem and link_elem.get("href"):
                href = link_elem["href"]
                link = "https://internshala.com" + href if href.startswith("/") else href
                jobs.append({"title": title, "link": link, "source": "Internshala"})
                print(f"   - {title[:50]}...")
        
        print(f"✅ Internshala: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Internshala failed: {e}")
        import traceback
        traceback.print_exc()
        return []

def linkedin_jobs():
    """LinkedIn Jobs - Public search page"""
    try:
        url = "https://www.linkedin.com/jobs/search/?keywords=data%20analyst%20intern&location=India"
        print(f"🔍 Fetching LinkedIn: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        print(f"   Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # LinkedIn job cards
        job_cards = soup.select("div.base-card")
        print(f"   Found {len(job_cards)} job cards")
        
        for card in job_cards[:10]:
            title_elem = card.select_one("h3")
            link_elem = card.select_one("a.base-card__full-link")
            
            if title_elem and link_elem:
                title = title_elem.get_text(strip=True)
                link = link_elem.get("href", "").split("?")[0]  # Remove tracking
                if link:
                    jobs.append({"title": title, "link": link, "source": "LinkedIn"})
                    print(f"   - {title[:50]}...")
        
        print(f"✅ LinkedIn: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ LinkedIn failed: {e}")
        import traceback
        traceback.print_exc()
        return []

def naukri_jobs():
    """Naukri - Indian job portal"""
    try:
        url = "https://www.naukri.com/data-analyst-intern-jobs"
        print(f"🔍 Fetching Naukri: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        print(f"   Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # Strategy 1: article.jobTuple
        job_articles = soup.select("article.jobTuple")
        print(f"   Strategy 1 (article.jobTuple): {len(job_articles)} found")
        
        if not job_articles:
            # Strategy 2: Any article
            job_articles = soup.find_all("article")
            print(f"   Strategy 2 (any article): {len(job_articles)} found")
        
        for article in job_articles[:10]:
            title_elem = article.select_one("a.title") or article.select_one("a")
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                if link and link.startswith("http"):
                    jobs.append({"title": title, "link": link, "source": "Naukri"})
                    print(f"   - {title[:50]}...")
        
        print(f"✅ Naukri: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Naukri failed: {e}")
        import traceback
        traceback.print_exc()
        return []

# ============ FILTERING ============

def is_da_role(title):
    """Smart filter for Data Analyst roles"""
    title_lower = title.lower()
    
    # Must contain at least one of these
    positive_keywords = [
        "data analyst",
        "business analyst",
        "analytics intern",
        "data analytics",
        "bi analyst"
    ]
    
    # Exclude these
    negative_keywords = [
        "senior", "lead", "manager", "director",
        "engineer", "scientist", "developer",
        "sales", "marketing", "hr"
    ]
    
    # Check positive
    has_positive = any(kw in title_lower for kw in positive_keywords)
    
    # Check negative
    has_negative = any(kw in title_lower for kw in negative_keywords)
    
    result = has_positive and not has_negative
    
    if not result:
        print(f"   ❌ FILTERED: {title[:60]}...")
    
    return result

def dedupe_jobs(jobs):
    """Remove duplicates by normalized title"""
    seen = set()
    unique = []
    
    for job in jobs:
        # Normalize title for comparison
        normalized = re.sub(r'[^a-z0-9]', '', job["title"].lower())
        
        if normalized not in seen:
            seen.add(normalized)
            unique.append(job)
        else:
            print(f"   🔄 DUPLICATE: {job['title'][:60]}...")
    
    return unique

def filter_jobs(jobs):
    """Filter and dedupe jobs"""
    print(f"\n📊 FILTERING {len(jobs)} total jobs...")
    
    # Filter by DA role
    filtered = [job for job in jobs if is_da_role(job["title"])]
    print(f"✅ After DA filter: {len(filtered)} jobs")
    
    # Remove duplicates
    unique = dedupe_jobs(filtered)
    print(f"✅ After dedup: {len(unique)} jobs")
    
    return unique

# ============ MAIN ============

def collect_all_jobs():
    """Collect from all sources"""
    print(f"\n{'='*60}")
    print(f"🚀 Starting job collection at {datetime.now()}")
    print(f"{'='*60}\n")
    all_jobs = []
    
    # Collect from each source with delays to avoid rate limits
    print("\n--- INDEED ---")
    indeed = indeed_jobs()
    all_jobs += indeed
    time.sleep(2)
    
    print("\n--- INTERNSHALA ---")
    internshala = internshala_jobs()
    all_jobs += internshala
    time.sleep(2)
    
    print("\n--- LINKEDIN ---")
    linkedin = linkedin_jobs()
    all_jobs += linkedin
    time.sleep(2)
    
    print("\n--- NAUKRI ---")
    naukri = naukri_jobs()
    all_jobs += naukri
    
    return all_jobs

def format_telegram_message(jobs):
    """Format jobs for Telegram"""
    if not jobs:
        return "⚠️ No Data Analyst internships found today.\n\nThe agent ran successfully but found no new matching roles."
    
    msg = f"🔥 <b>{len(jobs)} Data Analyst Opportunities</b>\n"
    msg += f"📅 {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
    
    for i, job in enumerate(jobs[:15], 1):  # Limit to 15 to avoid long messages
        msg += f"{i}. <b>{job['title']}</b>\n"
        msg += f"   📍 {job['source']}\n"
        msg += f"   🔗 {job['link']}\n\n"
    
    if len(jobs) > 15:
        msg += f"\n<i>+ {len(jobs) - 15} more jobs (visit sources directly)</i>"
    
    return msg

if __name__ == "__main__":
    # Step 1: Collect
    all_jobs = collect_all_jobs()
    print(f"\n{'='*60}")
    print(f"📊 COLLECTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total jobs collected: {len(all_jobs)}")
    
    # Step 2: Filter
    final_jobs = filter_jobs(all_jobs)
    
    # Step 3: Show breakdown by source
    print(f"\n📍 FINAL JOBS BY SOURCE:")
    sources = {}
    for job in final_jobs:
        sources[job['source']] = sources.get(job['source'], 0) + 1
    for source, count in sources.items():
        print(f"   {source}: {count} jobs")
    
    # Step 4: Send
    message = format_telegram_message(final_jobs)
    send_telegram(message)
    
    print(f"\n{'='*60}")
    print("✅ Done!")
    print(f"{'='*60}\n")
