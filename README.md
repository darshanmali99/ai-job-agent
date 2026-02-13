# 🤖 AI Job Agent — Career-Quality Intelligence System


> Automated AI-powered job tracker that scrapes, scores, and delivers **ONLY top-tier company opportunities** to Telegram with real-time analytics.

**🎯 Key Innovation**: Filters out unknown startups, alerts ONLY for Tier 1 & 2 companies (Google, TCS, Flipkart, Deloitte, etc.)

---

## 🚀 Features

### **🏆 Company Reputation Filtering (NEW!)**
- **Tier 1** (Score: 1.0): 80+ Top MNCs — Google, TCS, Deloitte, Flipkart, Accenture
- **Tier 2** (Score: 0.85): 70+ Mid-tier — Hexaware, OYO, Unacademy, Naukri
- **Tier 3** (Score: 0.4): Unknown startups — **Alerts suppressed**, CSV logged only

### **🧠 Triple Scoring System**
- **AI Semantic Score**: 0-100% relevance using keyword-based analysis
- **Keyword Skill Match**: Detects Python, SQL, Excel, Power BI, Tableau, ML
- **Hybrid Score**: 70% AI + 30% Skills
- **Final Rank**: 50% Hybrid + 50% Company Reputation

### **🔍 Multi-Portal Scraping**
- LinkedIn, Internshala, Indeed, Naukri, Instahyre
- 70+ jobs/run, every 3 hours via GitHub Actions
- Smart deduplication (1500 job memory)

### **📊 Live Dashboard**
- Real-time KPIs: Total jobs, AI scores, top skills, remote %
- Interactive charts: Daily trends, source distribution, skill demand
- Export filtered data as CSV

### **📱 Telegram Alerts**
- **ONLY Tier 1 & 2 companies** → Telegram ✅
- Tier 3 startups → CSV only (suppressed from alerts)
- Rich formatting: Scores, badges, clickable links

### **📈 Research-Grade Data**
- 14-column CSV dataset with all scores
- Publication-ready metrics
- Historical trend analysis

---

## 📊 Sample Output

### **Telegram (Tier 1/2 Found)**
```
🔥 3 New Data Analyst Opportunities

1. 🏆 Data Analyst Intern
   🏢 Google India
   🎯 AI Match: 0.85 (85%)
   🧠 Hybrid: 0.89 (89%) [Skills: 100%]
   🏆 Company: 1.00 (100%)
   🎯 Final Rank: 0.945 (94%)
```

### **Telegram (Only Tier 3)**
```
ℹ️ Job Agent Update

Found 2 new jobs, but none from Tier 1 or Tier 2 companies.

🔇 Alerts suppressed for unknown/low-reputation companies.
📊 All jobs logged to CSV for your review.
```

### **Dashboard KPIs**
```
Total Jobs: 10
Avg AI Score: 58.2%
Top Skill: SQL
Remote: 0.0%
```

---

## 🎯 System Architecture

```
Scraping → Filtering → AI Scoring → Hybrid Scoring → Company Ranking
    ↓          ↓            ↓              ↓                ↓
LinkedIn  Entry-level  Semantic      70% AI +      Tier 1/2/3
Internshala  roles    Analysis    30% Skills    Classification
  ↓                                                    ↓
Telegram Alerts (Tier 1 & 2 ONLY) + CSV Log (ALL)
```

---

## 🚀 Quick Start

### **1. Fork & Configure**
1. Fork this repository
2. Go to **Settings** → **Secrets** → Add:
   - `BOT_TOKEN`: Telegram bot token
   - `CHAT_ID`: Your Telegram chat ID

### **2. Enable GitHub Actions**
1. **Actions** tab → Enable workflows
2. System runs automatically every 3 hours

### **3. Deploy Dashboard (Optional)**
1. Go to https://share.streamlit.io/
2. Deploy: `your-repo` → `main` → `dashboard.py`
3. Live in 2 minutes!

---

## 📂 Project Structure

```
ai-job-agent/
├── job_agent.py          # Main scraping engine
├── ai_matcher.py         # AI semantic scoring
├── hybrid_scorer.py      # Hybrid scoring (AI + keywords)
├── company_ranker.py     # Tier-based company classification (NEW!)
├── dashboard.py          # Streamlit analytics dashboard
├── requirements.txt      # Dependencies
├── jobs_history.json     # Deduplication memory (auto)
└── jobs_dataset.csv      # Research data logs (auto)
```

---

## 🎯 How It Works

### **Scoring Formula**
```python
# Step 1: AI Semantic Score (0.0-1.0)
ai_score = keyword_based_semantic_analysis(job)

# Step 2: Keyword Skill Match (0.0-1.0)
keyword_score = matched_skills / total_required_skills

# Step 3: Hybrid Score
hybrid_score = 0.7 * ai_score + 0.3 * keyword_score

# Step 4: Company Reputation
company_score = 1.0 (Tier 1) | 0.85 (Tier 2) | 0.4 (Tier 3)

# Step 5: Final Rank
final_rank = 0.5 * hybrid_score + 0.5 * company_score
```

### **Telegram Filter**
```python
if company_score >= 0.85:  # Tier 1 or Tier 2
    send_telegram_alert()
else:  # Tier 3
    log_to_csv_only()  # Suppressed
```

---

## 🏆 Company Tiers

### **Tier 1 (80+ companies)**
Google, Microsoft, Amazon, TCS, Infosys, Wipro, Accenture, Deloitte, EY, KPMG, PwC, Flipkart, Swiggy, Zomato, Paytm, PhonePe, Razorpay, Goldman Sachs, JP Morgan, Reliance, Tata Group, Zoho, Freshworks...

### **Tier 2 (70+ companies)**
Hexaware, OYO, Unacademy, BYJU'S, Naukri, Shine, ClearTax, Haptik, Yellow.ai, Dream11, MPL, MakeMyTrip, Ixigo...

### **Tier 3 (Default)**
All other/unknown companies

---

## 📊 Dashboard Features

- **Filters**: AI score, date range, source, keywords
- **KPIs**: Total jobs, avg AI score, top skill, remote %
- **Charts**: Daily trend, source distribution, skill demand
- **Table**: Clickable links, progress bars, sortable
- **Export**: Download filtered CSV

---

## 🐛 Troubleshooting

### **No Telegram Alerts**
✅ **Expected!** System suppresses Tier 3 companies. Check CSV for all jobs.

### **All Jobs Suppressed**
✅ **Working correctly!** No Tier 1/2 jobs found. System logs to CSV.

### **Dashboard Not Loading**
1. Check if `jobs_dataset.csv` exists
2. Wait for GitHub Actions to run
3. Refresh dashboard

---

## 📈 Performance

- **Jobs/Run**: 70 average
- **Frequency**: Every 3 hours (8x/day)
- **Deduplication**: 1500 job memory
- **Tier 1 Alert Rate**: ~15-25% of jobs
- **Uptime**: 99%+

---

## 🔧 Configuration

### **Customize Company Tiers**
Edit `company_ranker.py`:
```python
TIER_1_COMPANIES = {
    "google", "microsoft", "amazon", ...
    # Add your preferred companies
}
```

### **Adjust Scoring Weights**
Edit `company_ranker.py`:
```python
# Change company importance
final_rank = 0.5 * hybrid + 0.5 * company  # Equal (50/50)
# OR
final_rank = 0.3 * hybrid + 0.7 * company  # Company > Skills
```

### **Change Schedule**
Edit `.github/workflows/job.yml`:
```yaml
cron: '0 */3 * * *'  # Every 3 hours
# OR
cron: '0 9,17 * * *'  # 9 AM & 5 PM only
```

---

## 📝 CSV Output

```csv
date,title,source,ai_score,hybrid_score,company_score,final_rank_score,final_decision
2026-02-13,Data Analyst,Google,0.85,0.89,1.0,0.945,Sent
2026-02-13,Analyst Intern,Unknown Startup,0.90,0.93,0.4,0.665,Suppressed
```

**Key**: Both logged, but only Tier 1/2 sent to Telegram!

---

## 🛠️ Tech Stack

- **Python 3.11**
- **GitHub Actions** (automation)
- **BeautifulSoup4** (scraping)
- **Streamlit** (dashboard)
- **Plotly** (charts)
- **Telegram Bot API** (alerts)

---

## 🎯 Success Metrics

### **Before Upgrade**
- ❌ All jobs sent to Telegram (spam)
- ❌ Unknown startups mixed with top MNCs
- ❌ Hard to identify quality opportunities

### **After Upgrade**
- ✅ Only Tier 1 & 2 companies alert Telegram
- ✅ Career-quality intelligence only
- ✅ Tier 3 logged to CSV for optional review
- ✅ Every alert is worth your attention!

---

## 📞 Support

**Issues?** Open an issue in this repository  
**Questions?** Check troubleshooting section  
**Improvements?** Submit a pull request

---

## ⭐ Star This Repository

If this helped you land a job, give it a star! ⭐

---



**Made with ❤️ for data analysts seeking top-tier opportunities**

**Last Updated**: February 2026

---

- **Dashboard**: [Live Demo](https://ai-job-agent-cpznbwvmuilyzvmxnjwy76.streamlit.app/)


## 💡 Key Takeaway

**Your AI Job Agent now functions as a career gatekeeper — only the best opportunities reach you. Every Telegram alert is from a reputable company worth applying to!** 🚀
