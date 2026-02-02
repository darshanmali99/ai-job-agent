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
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.content, "xml")
        jobs = []
        for item in soup.find_all("item")[:10]:
            title = item.title.text.strip()
            link = item.link.text.strip()
            jobs.append({"title": title, "link": link, "source": "Indeed"})
        print(f"✅ Indeed: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Indeed failed: {e}")
        return []

def internshala_jobs():
    """Internshala - Updated selectors for 2026"""
    try:
        url = "https://internshala.com/internships/data-analyst-internship/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # Updated selectors (check current HTML structure)
        # Try multiple patterns since Internshala changes frequently
        containers = (
            soup.select(".internship_meta") or
            soup.select(".individual_internship") or
            soup.select("div[class*='internship']")
        )
        
        for container in containers[:10]:
            # Find title
            title_elem = (
                container.select_one(".job-internship-name") or
                container.select_one("h3") or
                container.select_one("a")
            )
            if not title_elem:
                continue
                
            title = title_elem.get_text(strip=True)
            
            # Find link
            link_elem = container.select_one("a[href*='/internship/detail/']")
            if not link_elem:
                link_elem = container.find("a", href=True)
            
            if link_elem and link_elem.get("href"):
                link = "https://internshala.com" + link_elem["href"]
                jobs.append({"title": title, "link": link, "source": "Internshala"})
        
        print(f"✅ Internshala: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Internshala failed: {e}")
        return []

def linkedin_jobs():
    """LinkedIn Jobs - Public search page"""
    try:
        # LinkedIn public job search URL
        url = "https://www.linkedin.com/jobs/search/?keywords=data%20analyst%20intern&location=India"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # LinkedIn job cards
        job_cards = soup.select("div.base-card")[:10]
        for card in job_cards:
            title_elem = card.select_one("h3")
            link_elem = card.select_one("a.base-card__full-link")
            
            if title_elem and link_elem:
                title = title_elem.get_text(strip=True)
                link = link_elem.get("href", "").split("?")[0]  # Remove tracking
                if link:
                    jobs.append({"title": title, "link": link, "source": "LinkedIn"})
        
        print(f"✅ LinkedIn: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ LinkedIn failed: {e}")
        return []

def naukri_jobs():
    """Naukri - Indian job portal"""
    try:
        url = "https://www.naukri.com/data-analyst-intern-jobs"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        
        # Naukri job articles
        job_articles = soup.select("article.jobTuple")[:10]
        for article in job_articles:
            title_elem = article.select_one("a.title")
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                if link:
                    jobs.append({"title": title, "link": link, "source": "Naukri"})
        
        print(f"✅ Naukri: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Naukri failed: {e}")
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
    
    return has_positive and not has_negative

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
    
    return unique

def filter_jobs(jobs):
    """Filter and dedupe jobs"""
    # Filter by DA role
    filtered = [job for job in jobs if is_da_role(job["title"])]
    
    # Remove duplicates
    unique = dedupe_jobs(filtered)
    
    return unique

# ============ MAIN ============

def collect_all_jobs():
    """Collect from all sources"""
    print(f"🚀 Starting job collection at {datetime.now()}")
    all_jobs = []
    
    # Collect from each source with delays to avoid rate limits
    all_jobs += indeed_jobs()
    time.sleep(2)
    
    all_jobs += internshala_jobs()
    time.sleep(2)
    
    all_jobs += linkedin_jobs()
    time.sleep(2)
    
    all_jobs += naukri_jobs()
    
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
    print(f"📊 Total jobs collected: {len(all_jobs)}")
    
    # Step 2: Filter
    final_jobs = filter_jobs(all_jobs)
    print(f"✅ Jobs after filtering: {len(final_jobs)}")
    
    # Step 3: Send
    message = format_telegram_message(final_jobs)
    send_telegram(message)
    
    print("✅ Done!")
