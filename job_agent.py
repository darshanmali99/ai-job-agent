import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"
    requests.post(url, data={"chat_id": 1474889968, "text": msg[:3000]})

def scrape_internshala():
    url = "https://internshala.com/api/internships/search"

    params = {
        "profile": "data analyst",
        "location": "",
        "start_date": "",
        "duration": "",
        "stipend": "",
        "page": 1
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    jobs = []

    for item in data["internships"][:5]:
        title = item["title"]

        if "data" not in title.lower():
            continue

        company = item["company_name"]
        link = "https://internshala.com" + item["url"]

        jobs.append(
            f"🔹 {title}\n🏢 {company}\n🔗 {link}\n"
        )

    return jobs


if __name__ == "__main__":
    jobs = scrape_internshala()

    if not jobs:
        message = "⚠️ Scraper ran but found no jobs (site layout changed)."
    else:
        message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)

    send_telegram(message)
