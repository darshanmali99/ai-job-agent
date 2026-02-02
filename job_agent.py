import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def scrape_internshala():
    url = "https://internshala.com/internships/data-analyst-internship/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    cards = soup.find_all("div", class_="container-fluid individual_internship")

    for card in cards:
        title = card.find("a", class_="view_detail_button")
        company = card.find("p", class_="company_name")

        if title and company:
            title_text = title.text.strip()
            company_text = company.text.strip()
            link = "https://internshala.com" + title["href"]

            jobs.append(f"🔹 {title_text}\n🏢 {company_text}\n🔗 {link}\n")

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
