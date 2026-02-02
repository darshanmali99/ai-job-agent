import os
import re
import json
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# ============ CONFIG ============
# These will be loaded from GitHub Secrets automatically
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Location preferences (India-focused)
PREFERRED_LOCATIONS = [
    "remote", "work from home", "wfh",
    "india", "pune", "mumbai", "bangalore", "delhi", 
    "hyderabad", "chennai", "kolkata", "noida", "gurgaon"
]

# Keywords for filtering
INTERNSHIP_KEYWORDS = ["intern", "internship", "trainee", "fresher", "entry level", "entry-level"]
STIPEND_KEYWORDS = ["stipend", "paid", "₹", "rs.", "rs ", "inr", "salary", "compensation"]

# File paths
HISTORY_FILE = "jobs_history.json"
CSV_FILE = "jobs_dataset.csv"

# ============ LEVEL 1: MEMORY SYSTEM ============

def load_history():
    """Load sent jobs history from JSON file"""
    if not os.path.exists(HISTORY_FILE):
        return {"sent_links": [], "last_updated": None}
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict) or "sent_links" not in data:
                return {"sent_links": [], "last_updated": None}
            return data
    except Exception as e:
        print(f"⚠️ Error loading history: {e}")
        return {"sent_links": [], "last_updated": None}

def save_history(history):
    """Save sent jobs history to JSON file"""
    try:
        history["last_updated"] = datetime.now().isoformat()
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"💾 History saved: {len(history['sent_links'])} jobs tracked")
    except Exception as e:
        print(f"⚠️ Error saving history: {e}")

def is_new_job(link, history):
    """Check if job was already sent before"""
    return link not in history.get("sent_links", [])

def mark_as_sent(link, history):
    """Mark job as sent and maintain history size"""
    if "sent_links" not in history:
        history["sent_links"] = []
    
    history["sent_links"].append(link)
    
    # Keep only last 1000 jobs to prevent file bloat
    if len(history["sent_links"]) > 1000:
        history["sent_links"] = history["sent_links"][-1000:]

# ============ LEVEL 4: CSV DATASET ============

def init_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'date', 'title', 'source', 'link', 
                    'location', 'stipend_mentioned', 'easy_apply'
                ])
            print(f"📊 Created CSV dataset: {CSV_FILE}")
        except Exception as e:
            print(f"⚠️ Error creating CSV: {e}")

def save_to_csv(jobs):
    """Append jobs to CSV dataset"""
    if not jobs:
        return
    
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for job in jobs:
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d'),
                    job.get('title', 'N/A'),
                    job.get('source', 'N/A'),
                    job.get('link', 'N/A'),
                    job.get('location', 'N/A'),
                    job.get('has_stipend', False),
                    job.get('easy_apply', False)
                ])
        print(f"💾 Saved {len(jobs)} jobs to CSV dataset")
    except Exception as e:
        print(f"⚠️ Error saving to CSV: {e}")

# ============ TELEGRAM ============

def send_telegram(msg):
    """Send message to Telegram with error handling"""
    if not TOKEN or not CHAT_ID:
        print("❌ Telegram credentials missing (BOT_TOKEN or CHAT_ID)")
        print(f"   BOT_TOKEN present: {bool(TOKEN)}")
        print(f"   CHAT_ID present: {bool(CHAT_ID)}")
        return False
    
    try:
        response = requests.post(
            TELEGRAM_API,
            data={
                "chat_id": CHAT_ID, 
                "text": msg[:4000],
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Telegram message sent successfully")
            return True
        else:
            print(f"❌ Telegram failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

# ============ JOB SOURCES ============

def indeed_jobs():
    """Indeed RSS Feed - Most reliable source"""
    try:
        url = "https://in.indeed.com/rss?q=data+analyst+intern&l=India"
        print(f"🔍 Fetching Indeed...")
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "xml")
        jobs = []
        
        for item in soup.find_all("item")[:15]:
            try:
                title = item.title.text.strip() if item.title else ""
                link = item.link.text.strip() if item.link else ""
                description = item.description.text if item.description else ""
                
                if title and link:
                    jobs.append({
                        "title": title,
                        "link": link,
                        "source": "Indeed",
                        "description": description,
                        "location": "",
                        "stipend": ""
                    })
            except Exception as e:
                continue
        
        print(f"   ✅ Indeed: {len(jobs)} jobs found")
        return jobs
        
    except Exception as e:
        print(f"   ❌ Indeed failed: {e}")
        return []

def internshala_jobs():
    """Internshala - India's top internship platform"""
    try:
        url = "https://internshala.com/internships/data-analyst-internship/"
        print(f"🔍 Fetching Internshala...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        
        containers = (
            soup.select(".internship_meta") or
            soup.select(".individual_internship") or
            soup.find_all("div", class_=lambda x: x and "internship" in x.lower())
        )
        
        for container in containers[:15]:
            try:
                title_elem = (
                    container.select_one(".job-internship-name") or
                    container.select_one(".profile h3") or
                    container.select_one("h3") or
                    container.find("a")
                )
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link_elem = container.select_one("a[href*='/internship/detail/']") or container.find("a", href=True)
                
                if not link_elem or not link_elem.get("href"):
                    continue
                
                href = link_elem["href"]
                link = "https://internshala.com" + href if href.startswith("/") else href
                
                location_elem = container.select_one(".location_link")
                location = location_elem.get_text(strip=True) if location_elem else ""
                
                stipend_elem = container.select_one(".stipend")
                stipend = stipend_elem.get_text(strip=True) if stipend_elem else ""
                
                jobs.append({
                    "title": title,
                    "link": link,
                    "source": "Internshala",
                    "description": f"{location} {stipend}",
                    "location": location,
                    "stipend": stipend
                })
                
            except Exception as e:
                continue
        
        print(f"   ✅ Internshala: {len(jobs)} jobs found")
        return jobs
        
    except Exception as e:
        print(f"   ❌ Internshala failed: {e}")
        return []

def linkedin_jobs():
    """LinkedIn Jobs - Public search page"""
    try:
        url = "https://www.linkedin.com/jobs/search/?keywords=data%20analyst%20intern&location=India"
        print(f"🔍 Fetching LinkedIn...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        
        job_cards = soup.select("div.base-card")
        
        for card in job_cards[:15]:
            try:
                title_elem = card.select_one("h3")
                link_elem = card.select_one("a.base-card__full-link")
                
                if not title_elem or not link_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem.get("href", "").split("?")[0]
                
                if not link:
                    continue
                
                easy_apply = bool(
                    card.select_one(".job-card-container__apply-method") or
                    "easyApply" in card.get_text()
                )
                
                location_elem = card.select_one(".job-card-container__metadata-item")
                location = location_elem.get_text(strip=True) if location_elem else ""
                
                jobs.append({
                    "title": title,
                    "link": link,
                    "source": "LinkedIn",
                    "easy_apply": easy_apply,
                    "location": location,
                    "description": location,
                    "stipend": ""
                })
                
            except Exception as e:
                continue
        
        print(f"   ✅ LinkedIn: {len(jobs)} jobs found")
        return jobs
        
    except Exception as e:
        print(f"   ❌ LinkedIn failed: {e}")
        return []

def naukri_jobs():
    """Naukri.com - Leading Indian job portal"""
    try:
        url = "https://www.naukri.com/data-analyst-intern-jobs"
        print(f"🔍 Fetching Naukri...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        
        job_articles = soup.select("article.jobTuple") or soup.find_all("article")
        
        for article in job_articles[:15]:
            try:
                title_elem = article.select_one("a.title") or article.select_one("a")
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                
                if not link or not link.startswith("http"):
                    continue
                
                location_elem = article.select_one(".location")
                location = location_elem.get_text(strip=True) if location_elem else ""
                
                jobs.append({
                    "title": title,
                    "link": link,
                    "source": "Naukri",
                    "location": location,
                    "description": location,
                    "stipend": ""
                })
                
            except Exception as e:
                continue
        
        print(f"   ✅ Naukri: {len(jobs)} jobs found")
        return jobs
        
    except Exception as e:
        print(f"   ❌ Naukri failed: {e}")
        return []

# ============ FILTERING ============

def is_da_role(title):
    """Filter for Data Analyst roles only"""
    title_lower = title.lower()
    
    positive_keywords = [
        "data analyst", "business analyst", "analytics intern", 
        "data analytics", "bi analyst", "business intelligence"
    ]
    
    negative_keywords = [
        "senior", "sr.", "lead", "manager", "director", "head",
        "engineer", "scientist", "developer", "architect",
        "sales", "marketing", "hr", "recruiter"
    ]
    
    has_positive = any(kw in title_lower for kw in positive_keywords)
    has_negative = any(kw in title_lower for kw in negative_keywords)
    
    return has_positive and not has_negative

def is_internship_level(job):
    """Check if internship or entry-level role"""
    text = f"{job.get('title', '')} {job.get('description', '')}".lower()
    return any(kw in text for kw in INTERNSHIP_KEYWORDS)

def has_location_match(job):
    """Check if location matches preferences"""
    text = f"{job.get('title', '')} {job.get('description', '')} {job.get('location', '')}".lower()
    return any(loc in text for loc in PREFERRED_LOCATIONS)

def check_stipend(job):
    """Check if stipend is mentioned"""
    text = f"{job.get('description', '')} {job.get('stipend', '')}".lower()
    has_stipend = any(kw in text for kw in STIPEND_KEYWORDS)
    
    if "unpaid" in text:
        return False
    
    return has_stipend

def enhance_job(job):
    """Add metadata to job"""
    job['is_internship'] = is_internship_level(job)
    job['location_match'] = has_location_match(job)
    job['has_stipend'] = check_stipend(job)
    job['easy_apply'] = job.get('easy_apply', False)
    
    return job

def filter_jobs(jobs, history):
    """Master filter applying all levels"""
    filtered = []
    
    for job in jobs:
        if not is_new_job(job.get('link', ''), history):
            continue
        
        if not is_da_role(job.get('title', '')):
            continue
        
        if not is_internship_level(job):
            continue
        
        job = enhance_job(job)
        filtered.append(job)
    
    return filtered

def dedupe_jobs(jobs):
    """Remove duplicate jobs"""
    seen = set()
    unique = []
    
    for job in jobs:
        normalized = re.sub(r'[^a-z0-9]', '', job.get("title", "").lower())
        
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique.append(job)
    
    return unique

# ============ MAIN ============

def collect_all_jobs():
    """Collect jobs from all sources"""
    print(f"\n{'='*70}")
    print(f"🚀 Job Collection Started: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print(f"{'='*70}\n")
    
    all_jobs = []
    
    all_jobs += indeed_jobs()
    time.sleep(2)
    
    all_jobs += internshala_jobs()
    time.sleep(2)
    
    all_jobs += linkedin_jobs()
    time.sleep(2)
    
    all_jobs += naukri_jobs()
    
    print(f"\n{'='*70}")
    print(f"📊 Total jobs collected: {len(all_jobs)}")
    print(f"{'='*70}")
    
    return all_jobs

def format_telegram_message(jobs):
    """Format jobs for Telegram"""
    if not jobs:
        return (
            "⚠️ <b>No New Jobs Today</b>\n\n"
            "All recent Data Analyst internship postings were already sent to you!\n\n"
            "✅ Agent ran successfully.\n"
            f"🕐 {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        )
    
    msg = f"🔥 <b>{len(jobs)} New Data Analyst Opportunities</b>\n"
    msg += f"📅 {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
    msg += f"{'─'*40}\n\n"
    
    for i, job in enumerate(jobs[:15], 1):
        star = "⭐ " if job.get('easy_apply') else ""
        stipend = "💰 " if job.get('has_stipend') else ""
        location_icon = "📍 " if job.get('location_match') else ""
        
        msg += f"{i}. {star}{stipend}{location_icon}<b>{job['title']}</b>\n"
        msg += f"   🏢 {job['source']}"
        
        if job.get('location'):
            msg += f" • {job['location']}"
        
        msg += f"\n   🔗 {job['link']}\n\n"
    
    if len(jobs) > 15:
        msg += f"<i>...and {len(jobs) - 15} more opportunities!</i>\n\n"
    
    msg += f"\n{'─'*40}\n"
    msg += "💡 <b>Legend:</b>\n"
    msg += "⭐ Easy Apply • 💰 Stipend Mentioned • 📍 Preferred Location"
    
    return msg

def main():
    """Main execution"""
    try:
        init_csv()
        history = load_history()
        
        print(f"📚 Memory loaded: {len(history.get('sent_links', []))} jobs in history")
        
        all_jobs = collect_all_jobs()
        
        print(f"\n🔍 Filtering jobs...")
        filtered_jobs = filter_jobs(all_jobs, history)
        print(f"   ✅ After filtering: {len(filtered_jobs)} jobs")
        
        final_jobs = dedupe_jobs(filtered_jobs)
        print(f"   ✅ After deduplication: {len(final_jobs)} jobs")
        
        if final_jobs:
            save_to_csv(final_jobs)
            
            for job in final_jobs:
                mark_as_sent(job.get('link', ''), history)
            save_history(history)
            
            message = format_telegram_message(final_jobs)
            send_telegram(message)
            
            print(f"\n{'='*70}")
            print(f"✅ SUCCESS: Sent {len(final_jobs)} new jobs to Telegram")
            
            sources = {}
            for job in final_jobs:
                source = job.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\n📊 Jobs by source:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {source}: {count} jobs")
            
            print(f"{'='*70}\n")
            
        else:
            message = format_telegram_message([])
            send_telegram(message)
            
            print(f"\n{'='*70}")
            print(f"ℹ️  No new jobs found")
            print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"❌ CRITICAL ERROR: {e}")
        print(f"{'='*70}\n")
        
        error_msg = (
            f"⚠️ <b>Job Agent Error</b>\n\n"
            f"The agent encountered an error:\n"
            f"<code>{str(e)[:200]}</code>\n\n"
            f"🕐 {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        )
        send_telegram(error_msg)
        
        raise

if __name__ == "__main__":
    main()
