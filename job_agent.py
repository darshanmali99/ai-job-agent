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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for card in soup.select(".individual_internship"):
        title = card.select_one("h3")
        company = card.select_one(".company_name")
        link = card.select_one("a")

        if title and company and link:
            title_text = title.text.strip()
            company_text = company.text.strip()
            link_text = "https://internshala.com" + link["href"]

            jobs.append(
                f"🔹 {title_text}\n🏢 {company_text}\n🔗 {link_text}\n"
            )

        if len(jobs) == 5:
            break

    return jobs


if __name__ == "__main__":
    jobs = scrape_internshala()
    message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)
    send_telegram(message)
