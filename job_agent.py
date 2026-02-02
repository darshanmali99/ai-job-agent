import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY}/sendMessage"
    data = {
        "chat_id":1474889968,
        "text": msg[:3000]
    }
    r = requests.post(url, data=data)
    print("TELEGRAM RESPONSE:", r.text)

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
    send_telegram("HELLO FROM GITHUB AGENT")

    jobs = scrape_internshala()
    print("JOBS FOUND:", len(jobs))

    message = "TEST MESSAGE FROM AGENT"

    send_telegram(message)
