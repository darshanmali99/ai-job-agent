🚀 AI Job Agent — Data Analyst Internship Intelligence Bot

An automated AI-powered job intelligence system that collects, filters, deduplicates, analyzes, and delivers Data Analyst / Business Analyst internship opportunities from multiple job portals directly to Telegram — running fully autonomously via GitHub Actions.

This is not a simple scraper.
This is a job intelligence pipeline with memory, filtering logic, dataset creation, and automation.

🎯 Purpose

Finding quality Data Analyst internships across portals daily is time-consuming and repetitive.

This project solves that by:

Scanning multiple job portals automatically

Filtering only relevant entry-level Data/BA roles

Removing duplicates across days

Tracking history of sent jobs

Building a dataset of opportunities over time

Sending only new, relevant jobs to Telegram

🧠 System Architecture
Job Portals → Scraper Layer → Filtering Engine → Memory Check →
Dataset Storage (CSV/JSON) → Telegram Delivery → GitHub Actions Automation

🌐 Job Sources Covered

Indeed (RSS)

Internshala

LinkedIn Jobs (public search)

Naukri.com

Instahyre

Multiple queries per portal are used to maximize coverage.

⚙️ Core Features Implemented
✅ Multi-Portal Scraping

Collects jobs from 5+ portals with multiple search variations.

✅ Smart Role Filtering

Identifies only:

Data Analyst

Business Analyst

Analytics Intern

Entry-level / Intern roles

Excludes senior/irrelevant roles.

✅ Location Intelligence

Matches jobs against preferred Indian cities + Remote/WFH.

✅ Stipend Detection

Detects if stipend/salary is mentioned.

✅ Easy Apply Detection (LinkedIn)
✅ Deduplication Engine

Removes duplicate jobs across portals using normalized title matching.

✅ Memory System (jobs_history.json)

Never sends the same job twice across days.

✅ Dataset Creation (jobs_dataset.csv)

Every job is logged for future analysis and research.

✅ Telegram Automation

Sends formatted, ranked job list automatically.

✅ Fully Automated via GitHub Actions

Runs daily without any manual effort.

📁 Project Structure
ai-job-agent/
│
├── job_agent.py           # Main intelligence & scraping engine
├── jobs_history.json      # Memory of sent jobs
├── jobs_dataset.csv       # Dataset of all collected jobs
└── .github/workflows/
    └── job.yml            # GitHub Actions automation

🔐 Environment Variables (GitHub Secrets)

Set these in Settings → Secrets → Actions

Secret Name	Description
BOT_TOKEN	Telegram Bot token from BotFather
CHAT_ID	Your Telegram chat ID
▶️ How It Works Daily

GitHub Action triggers the script

Jobs collected from all portals

Filtering engine selects only relevant internships

Duplicate & previously sent jobs removed

New jobs saved to CSV dataset

Memory updated

Telegram message sent with only new jobs

📊 Dataset Advantage

The CSV file grows daily and enables:

Analysis of hiring trends

Best cities for internships

Which portal posts most jobs

% of jobs with stipend

Company hiring patterns

This transforms the project from automation → data intelligence.

📩 Telegram Output Example
🔥 12 New Data Analyst Opportunities
📅 02 Feb 2026, 01:03 PM

⭐ 💰 📍 Data Analyst Intern
🏢 LinkedIn • Bangalore
🔗 link


Legend:

⭐ Easy Apply

💰 Stipend

📍 Preferred Location

🛠 Tech Stack

Python

BeautifulSoup

Requests

GitHub Actions (CI/CD automation)

Telegram Bot API

CSV / JSON for data persistence

🚀 What Makes This Project Special

This is not a basic scraper. It includes:

Data engineering concepts

Automation pipeline

Stateful memory system

Real-time filtering intelligence

Dataset generation for analytics

Production-style error handling

📌 Future Enhancements (Planned)

Job scoring & ranking engine

Company name extraction

Weekly analytics summary

Portal health monitoring

README auto-stats from dataset

👨‍💻 Author

Darshan Mali
B.Tech Computer Science | Data Analyst Enthusiast
Built as a real-world automation + data intelligence project.

⭐ Why This Project Matters

This project demonstrates:

Automation thinking

Data collection & cleaning

Intelligent filtering

CI/CD usage

Practical problem solving

Dataset generation for research

A perfect blend of Data Engineering + Automation + Analytics
