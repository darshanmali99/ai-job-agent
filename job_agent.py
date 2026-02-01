import requests
from bs4 import BeautifulSoup

TOKEN = "PASTE_YOUR_TOKEN"
CHAT_ID = "PASTE_YOUR_CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def scrape_internshala():
    url = "https://internshala.com/internships/data-analyst-internship/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    for card in soup.find_all("div", class_="individual_internship"):
        title = card.find("h3").text.strip()
        company = card.find("h4").text.strip()
        link = "https://internshala.com" + card.find("a")["href"]

        jobs.append(f"{title}\n{company}\n{link}\n")

    return jobs[:5]

if __name__ == "__main__":
    jobs = scrape_internshala()
    message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)
    send_telegram(message)
