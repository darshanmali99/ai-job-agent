import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"
    requests.post(url, data={"chat_id": 1474889968, "text": msg[:3500]})


# ------------------ SOURCE 1: Indeed ------------------
def get_indeed_jobs():
    url = "https://in.indeed.com/jobs?q=data+analyst+intern&l=India"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    for a in soup.select("a.tapItem"):
        title = a.select_one("h2").text.strip()
        link = "https://in.indeed.com" + a["href"]

        jobs.append((title, link))

        if len(jobs) == 5:
            break

    return jobs


# ------------------ SOURCE 2: Internshala (search page) ------------------
def get_internshala_jobs():
    url = "https://internshala.com/internships/keywords-data-analyst/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    for card in soup.select("div.individual_internship"):
        title = card.select_one("h3").text.strip()
        link = "https://internshala.com" + card.select_one("a")["href"]

        jobs.append((title, link))

        if len(jobs) == 5:
            break

    return jobs


# ------------------ SOURCE 3: Wellfound (AngelList) ------------------
def get_wellfound_jobs():
    url = "https://wellfound.com/jobs?query=data%20analyst%20intern"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    for a in soup.select("a[href*='/jobs/']"):
        title = a.text.strip()
        link = "https://wellfound.com" + a["href"]

        jobs.append((title, link))

        if len(jobs) == 5:
            break

    return jobs


# ------------------ FILTER + DEDUPE ------------------
def filter_and_dedupe(all_jobs):
    seen = set()
    filtered = []

    for title, link in all_jobs:
        key = title.lower()

        if "data" not in key:
            continue

        if key in seen:
            continue

        seen.add(key)
        filtered.append((title, link))

    return filtered[:10]


# ------------------ MAIN AGENT ------------------
if __name__ == "__main__":
    all_jobs = []

    all_jobs += get_indeed_jobs()
    all_jobs += get_internshala_jobs()
    all_jobs += get_wellfound_jobs()

    final_jobs = filter_and_dedupe(all_jobs)

    if not final_jobs:
        message = "⚠️ Agent ran but no jobs found today."
    else:
        message = "🔥 Latest Data Analyst Internships & Jobs:\n\n"
        for title, link in final_jobs:
            message += f"🔹 {title}\n🔗 {link}\n\n"

    send_telegram(message)
