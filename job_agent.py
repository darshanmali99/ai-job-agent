import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"
    requests.post(url, data={"chat_id": 1474889968, "text": msg[:3000]})

def scrape_internshala():
    url = "https://internshala.com/internships/data-analyst-internship/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    cards = soup.select("div.internship_meta")

    for card in cards:
        title_tag = card.select_one("a.job-title-href")
        company_tag = card.select_one("div.company_name")
        link_tag = card.select_one("a.job-title-href")

        if title_tag and company_tag and link_tag:
    title = title_tag.text.strip()

    if "data" not in title.lower():
        continue

            title = title_tag.text.strip()
            company = company_tag.text.strip()
            link = "https://internshala.com" + link_tag["href"]

            jobs.append(
                f"🔹 {title}\n🏢 {company}\n🔗 {link}\n"
            )

        if len(jobs) == 5:
            break

    return jobs



if __name__ == "__main__":
    jobs = scrape_internshala()

    if not jobs:
        message = "⚠️ Scraper ran but found no jobs (site layout changed)."
    else:
        message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)

    send_telegram(message)
