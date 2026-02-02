import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"
    requests.post(url, data={"chat_id": 1474889968, "text": msg[:3500]})


# ---------------- INDEED RSS (never breaks) ----------------
def indeed_jobs():
    url = "https://in.indeed.com/rss?q=data+analyst+intern&l=India"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "xml")

    jobs = []
    for item in soup.find_all("item")[:5]:
        title = item.title.text
        link = item.link.text
        jobs.append((title, link))
    return jobs


# ---------------- INTERNSHALA SEARCH PAGE (light HTML) ----------------
def internshala_jobs():
    url = "https://internshala.com/internships/keywords-data-analyst/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    for a in soup.select("a[href*='/internship/detail/']")[:5]:
        title = a.text.strip()
        link = "https://internshala.com" + a["href"]
        jobs.append((title, link))
    return jobs


# ---------------- REMOTEOK (JSON page) ----------------
def remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).json()

    jobs = []
    for job in data:
        if isinstance(job, dict) and "data" in job.get("position", "").lower():
            title = job["position"]
            link = "https://remoteok.com" + job["url"]
            jobs.append((title, link))

        if len(jobs) == 5:
            break

    return jobs


# ---------------- FILTER ----------------
def filter_jobs(jobs):
    seen = set()
    result = []

    for title, link in jobs:
        key = title.lower()
        if "data" not in key:
            continue
        if key in seen:
            continue

        seen.add(key)
        result.append((title, link))

    return result[:10]


# ---------------- MAIN ----------------
if __name__ == "__main__":
    all_jobs = []
    all_jobs += indeed_jobs()
    all_jobs += internshala_jobs()
    all_jobs += remoteok_jobs()

    final = filter_jobs(all_jobs)

    if not final:
        send_telegram("⚠️ Agent ran but no jobs found today.")
    else:
        msg = "🔥 Latest Data Analyst Internships & Jobs:\n\n"
        for t, l in final:
            msg += f"🔹 {t}\n🔗 {l}\n\n"
        send_telegram(msg)
