import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY")
CHAT_ID = os.getenv("1474889968")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8200332646:AAFwPeYI9t_YVCjkp37CaW8AMxzxSWIM9HY/sendMessage"
    requests.post(url, data={"chat_id": 1474889968, "text": msg[:3000]})

import feedparser
import requests

def scrape_jobs():
    url = "https://in.indeed.com/rss?q=data+analyst+intern&l=India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    feed = feedparser.parse(response.text)

    jobs = []

    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link

        jobs.append(
            f"🔹 {title}\n🔗 {link}\n"
        )

    return jobs



if __name__ == "__main__":
    jobs = scrape_jobs()
    message = "🔥 Latest Data Analyst Internships:\n\n" + "\n".join(jobs)
    send_telegram(message)
