import requests
from bs4 import BeautifulSoup

TOKEN = "8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY"
CHAT_ID = "1474889968"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def scrape_internshala():
    url = "https://internshala.com/internships/data-analyst-internship/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    cards = soup.find_all("div", class_="individual_internship")

    for card in cards[:5]:
        title_tag = card.find("h3")
        company_tag = card.find("h4")
        link_tag = card.find("a", href=True)

        if title_tag and company_tag and link_tag:
            title = title_tag.text.strip()
            company = company_tag.text.strip()
            link = "https://internshala.com" + link_tag["href"]

            job_text = f"🔹 {title}\n🏢 {company}\n🔗 {link}\n"
            jobs.append(job_text)

    return jobs

if __name__ == "__main__":
    jobs = scrape_internshala()
    message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)
    send_telegram(message)
