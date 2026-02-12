# 🤖 AI Job Agent — Intelligent Data Analyst Internship Tracker


> An automated, AI-powered job intelligence system that scrapes, filters, scores, and delivers Data Analyst and Business Analyst internship opportunities with real-time analytics dashboard.

![Dashboard Preview](https://img.shields.io/badge/Live-Dashboard-success)

---

## 🎯 Features

### **🔍 Multi-Portal Job Scraping**
- **5 Job Portals**: LinkedIn, Internshala, Indeed, Naukri, Instahyre
- **Automated Scraping**: Runs every 3 hours via GitHub Actions
- **Smart Filtering**: Entry-level data analyst roles only
- **70+ Jobs/Run**: Comprehensive coverage of opportunities

### **🧠 AI-Powered Intelligence**
- **Semantic AI Scoring** (0-100%): Keyword-based semantic analysis
- **Skill Detection**: Python, SQL, Excel, Power BI, Tableau, Machine Learning
- **Hybrid Scoring**: 70% AI semantic + 30% keyword skill matching
- **Smart Ranking**: Jobs sorted by relevance score

### **📊 Real-Time Analytics Dashboard**
- **Live Streamlit Dashboard**: Interactive data visualization
- **Executive KPIs**: Total jobs, avg scores, top skills, remote %
- **Advanced Charts**: Trend analysis, source distribution, skill demand
- **Filtering**: By date, source, AI score, keywords
- **Export**: Download filtered data as CSV

### **📱 Instant Telegram Alerts**
- **Real-Time Notifications**: New jobs delivered immediately
- **Rich Formatting**: Emojis, scores, and clickable links
- **Score Indicators**: 🎯 Excellent (70%+) • ✅ Good (50%+) • ⚡ Moderate • 🔍 Low
- **Smart Filtering**: Only relevant matches

### **📈 Research-Grade Data Logging**
- **CSV Dataset**: All jobs logged with scores and metadata
- **12 Data Fields**: Date, title, source, link, location, stipend, scores, decision
- **Publication-Ready**: Metrics for academic research and analysis
- **Deduplication**: Tracks 1500+ job history

### **⚙️ Production-Grade Automation**
- **GitHub Actions**: Fully automated, zero maintenance
- **CPU-Only**: No GPU or ML dependencies required
- **Graceful Degradation**: System works even if components fail
- **Error Handling**: Robust error recovery and logging

---

## 📊 Live Dashboard

**Access the dashboard**: [[Your Streamlit App URL](https://ai-job-agent-cpznbwvmuilyzvmxnjwy76.streamlit.app/)]

### Dashboard Features:
- 📊 **Executive KPIs**: Jobs tracked, AI scores, top skills, remote %
- 📈 **Trend Analysis**: Jobs per day line chart
- 🎯 **Source Distribution**: Donut chart by portal
- 💻 **Skill Demand**: Bar chart for top technical skills
- 📋 **Job Details**: Interactive table with clickable links
- 💾 **Export**: Download filtered data


---

## 📈 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS (Every 3h)                  │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   LinkedIn   │    │  Internshala │    │    Indeed    │ │
│  │   Naukri     │    │  Instahyre   │    │              │ │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘ │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              ▼                                │
│                    ┌─────────────────┐                       │
│                    │  Job Scraper    │                       │
│                    │  (job_agent.py) │                       │
│                    └────────┬────────┘                       │
│                             │                                 │
│         ┌───────────────────┼───────────────────┐            │
│         ▼                   ▼                   ▼            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Keyword    │  │  AI Semantic │  │    Hybrid    │      │
│  │   Filtering  │  │   Scoring    │  │   Scoring    │      │
│  │              │  │ (ai_matcher) │  │ (70% AI +    │      │
│  │              │  │              │  │  30% Skills) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│         └──────────────────┼──────────────────┘               │
│                            ▼                                  │
│                  ┌──────────────────┐                        │
│                  │  Deduplication   │                        │
│                  │ (1500 job memory)│                        │
│                  └────────┬─────────┘                        │
│                           │                                   │
│           ┌───────────────┼───────────────┐                  │
│           ▼               ▼               ▼                  │
│    ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│    │  Telegram  │  │  CSV Log   │  │  Streamlit │          │
│    │   Alert    │  │  Dataset   │  │ Dashboard  │          │
│    └────────────┘  └────────────┘  └────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### **Prerequisites**
- GitHub account
- Telegram account
- Streamlit Cloud account (free)

### **Step 1: Create Telegram Bot**

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy your bot token (looks like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)
4. Get your chat ID:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Copy the `chat.id` value

### **Step 2: Fork & Configure Repository**

1. **Fork this repository** to your GitHub account
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add two secrets:
   - `BOT_TOKEN`: Your Telegram bot token
   - `CHAT_ID`: Your Telegram chat ID

### **Step 3: Enable GitHub Actions**

1. Go to **Actions** tab
2. Click **"I understand my workflows, go ahead and enable them"**
3. The bot will now run automatically every 3 hours!

### **Step 4: Deploy Dashboard (Optional)**

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `your-username/ai-job-agent`
   - Branch: `main`
   - Main file path: `dashboard.py`
5. Click "Deploy"
6. Your dashboard will be live in 2-3 minutes!

### **Step 5: Manual Test Run (Optional)**

1. Go to **Actions** tab
2. Click **"Job Agent"** workflow
3. Click **"Run workflow"** button
4. Check your Telegram for job alerts!

---

## 📊 Sample Output

### **Telegram Alert**
```
🔥 4 New Data Analyst Opportunities
📅 09 Feb 2026, 09:55 AM
────────────────────────────────────────

1. Data Analyst Intern (Excel, SQL, Power BI)
   🏢 LinkedIn
   🎯 AI Match: 1.00 (100%)
   🧠 Hybrid Match: 1.00 (100%) [Skills: 100%]
   🔗 https://in.linkedin.com/jobs/view/...

2. Business Analyst Intern
   🏢 LinkedIn
   ⚡ AI Match: 0.48 (48%)
   🧠 Hybrid Match: 0.49 (49%) [Skills: 50%]
   🔗 https://in.linkedin.com/jobs/view/...

────────────────────────────────────────
💡 Legend:
⭐ Easy Apply • 💰 Stipend • 📍 Preferred Location
🎯 Excellent (70%+) • ✅ Good (50%+) • ⚡ Moderate • 🔍 Low
🧠 Hybrid = 70% AI + 30% Skills Match
```

### **Dashboard KPIs**
```
📊 Executive KPIs
────────────────────────────────────────
Total Jobs Tracked: 85
Average AI Score: 52%
Top Skill in Demand: SQL (45 jobs)
Remote Opportunities: 30.5% (26 jobs)
```

### **CSV Dataset**
```csv
date,title,source,link,location,stipend_mentioned,easy_apply,ai_score,keyword_score,hybrid_score,keyword_pass,final_decision
2026-02-09,Data Analyst Intern (Excel SQL Power BI),LinkedIn,https://...,Remote,False,False,1.00,1.00,1.00,True,Sent
2026-02-09,Business Analyst Intern,LinkedIn,https://...,Pune,False,False,0.48,0.50,0.49,True,Sent
```

---

## 🎯 How AI Scoring Works

### **AI Semantic Scoring (0.0 - 1.0)**

Keyword-based semantic matching to score job relevance:

```python
Score = (High Priority Skills × 0.20) + 
        (Full Text Matches × 0.10) + 
        (Medium Priority × 0.08) + 
        (Positive Keywords × 0.05) + 
        (Entry-Level Bonus × 0.10)
```

**High Priority Skills** (0.20 each, max 0.80):
- `data analyst`, `business analyst`, `sql`, `python`, `excel`, `power bi`, `tableau`

**Medium Priority** (0.08 each, max 0.30):
- `intern`, `internship`, `entry level`, `junior`, `fresher`, `dashboard`, `reporting`

**Positive Keywords** (0.05 each, max 0.15):
- `remote`, `paid`, `stipend`, `training`, `statistics`, `machine learning`

**Entry-Level Bonus** (+0.10):
- Triggered if job title contains: `intern`, `internship`, `entry level`, `junior`

---

### **Keyword Skill Matching (0.0 - 1.0)**

Detects required technical skills in job descriptions:

```
Keyword Score = (Matched Skills) / (Total Required Skills)
```

**Detected Skills**: Python, SQL, Excel, Power BI, Tableau, Pandas, NumPy, R, Statistics, Machine Learning, ETL, Data Visualization, MySQL, PostgreSQL

---

### **Hybrid Score Formula**

```
Hybrid Score = (0.7 × AI Score) + (0.3 × Keyword Score)
```

**Why 70/30?**
- AI semantic understanding is weighted higher (70%)
- Specific skill matching provides validation (30%)
- Balances general relevance with technical requirements

---

## 📂 Project Structure

```
ai-job-agent/
├── .github/
│   └── workflows/
│       ├── job.yml              # Main automation (every 3h)
│       └── test.yml             # Testing workflow (manual)
├── job_agent.py                 # Main scraping engine
├── ai_matcher.py                # AI semantic scoring
├── hybrid_scorer.py             # Hybrid scoring (AI + Keywords)
├── dashboard.py                 # Streamlit analytics dashboard
├── test_scoring.py              # Diagnostic testing
├── requirements.txt             # Python dependencies
├── jobs_history.json            # Deduplication memory (auto)
├── jobs_dataset.csv             # Research data logs (auto)
└── README.md                    # This file
```

---

## 🔧 Configuration

### **Customize Your Profile**

Edit `hybrid_scorer.py` to match your skills:

```python
# Default user profile (line 76)
user_skills = [
    "python", "sql", "excel", "power bi", "tableau",
    "pandas", "data visualization", "statistics"
]
```

### **Adjust Scoring Weights**

Edit `hybrid_scorer.py` (line 24-25):

```python
AI_WEIGHT = 0.7        # Change to 0.8 for more AI emphasis
KEYWORD_WEIGHT = 0.3   # Change to 0.2 to reduce keyword importance
```

### **Change Schedule**

Edit `.github/workflows/job.yml` (line 4):

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours (current)
  # - cron: '0 9,17 * * *'  # Twice daily at 9 AM and 5 PM
  # - cron: '0 9 * * 1-5'   # Weekdays only at 9 AM
```

### **Filter Location**

Edit `job_agent.py` (line 36-43):

```python
PREFERRED_LOCATIONS = [
    "remote", "pune", "mumbai", "bangalore",
    # Add more cities here
]
```

---

## 🧪 Testing

### **Run Diagnostic Test**

```bash
python test_scoring.py
```

**Expected Output:**
```
✅ AI matcher import: SUCCESS
✅ Hybrid scorer import: SUCCESS
======================================================================
TESTING AI + HYBRID SCORING
======================================================================
AI matcher initializing...
   AI matcher ready
AI scoring 2 jobs...
   Scored: 2/2 jobs
   Average score: 0.740

Job 1: Data Analyst Intern (Excel, SQL, Power BI)
  AI Score:     1.0
  Keyword Score: 1.0
  Hybrid Score:  1.0

✅ SUCCESS: AI scoring is working correctly!
```

### **Test Dashboard Locally**

```bash
streamlit run dashboard.py
```

Opens browser at `http://localhost:8501`

---

## 📊 Dashboard Usage

### **Filters**
- **Min AI Score**: Slider (0.0-1.0) to filter by relevance
- **Date Range**: Select start and end dates
- **Job Portals**: Multi-select LinkedIn, Internshala, etc.
- **Search**: Keyword search in title/location

### **KPIs**
- **Total Jobs Tracked**: Count of filtered jobs
- **Average AI Score**: Mean AI relevance (%)
- **Top Skill in Demand**: Most mentioned technical skill
- **Remote Opportunities**: % of remote/WFH jobs

### **Charts**
- **Daily Trend**: Line chart showing jobs posted per day
- **Source Distribution**: Donut chart of jobs by portal
- **Skill Demand**: Bar chart of technical skills mentioned

### **Data Table**
- **Interactive**: Click job links to apply
- **Progress Bars**: Visual AI/Hybrid scores
- **Sortable**: Click column headers to sort

### **Export**
- Click "Download CSV" to export filtered data
- Timestamped filename for easy tracking

---

## 📈 Performance Metrics

### **Current System Performance**
- **Jobs Scraped**: 70 per run (LinkedIn: 40, Internshala: 30)
- **Run Frequency**: Every 3 hours (8 times/day)
- **Deduplication**: 1500 job memory
- **Success Rate**: 99%+ uptime
- **Average AI Score**: 52% (moderate relevance)
- **Average Hybrid Score**: 55%

### **Score Distribution**
- 🎯 Excellent (70%+): ~25% of jobs
- ✅ Good (50-69%): ~25% of jobs
- ⚡ Moderate (30-49%): ~40% of jobs
- 🔍 Low (<30%): ~10% of jobs

---

## 📊 Data Analysis

### **Basic Statistics**

```python
import pandas as pd

# Load dataset
df = pd.read_csv('jobs_dataset.csv')

# Score distribution
print(f"Average AI Score: {df['ai_score'].mean():.2f}")
print(f"Average Hybrid Score: {df['hybrid_score'].mean():.2f}")

# High-quality jobs
excellent = df[df['hybrid_score'] >= 0.70]
print(f"Excellent matches: {len(excellent)} ({len(excellent)/len(df)*100:.1f}%)")
```

### **Portal Quality Analysis**

```python
# Which portal has best jobs?
portal_scores = df.groupby('source')[['ai_score', 'hybrid_score']].mean()
print(portal_scores.sort_values('hybrid_score', ascending=False))
```

### **Skill Gap Analysis**

```python
# Jobs where you're missing skills
skill_gap = df[(df['ai_score'] > 0.6) & (df['keyword_score'] < 0.5)]
print(f"Jobs requiring more skills: {len(skill_gap)}")
print(skill_gap[['title', 'source', 'ai_score', 'keyword_score']])
```

---

## 🐛 Troubleshooting

### **No Jobs Appearing**

**Cause**: All scraped jobs are duplicates (already in history)

**Solution**: Wait for new jobs to be posted. System runs every 3 hours.

---

### **AI Scores Missing**

**Cause**: `ai_matcher.py` not loading properly

**Solution**: 
1. Check GitHub Actions logs for: `✅ AI matcher module loaded`
2. If you see `⚠️ AI matcher disabled`, re-upload `ai_matcher.py`
3. Run test: `python test_scoring.py`

---

### **Dashboard Not Loading Data**

**Cause**: CSV file missing or malformed

**Solution**:
1. Check if `jobs_dataset.csv` exists in repository
2. Verify it has correct header (12 columns)
3. Delete and let GitHub Actions regenerate it

---

### **Telegram Not Working**

**Cause**: Invalid bot token or chat ID

**Solution**:
1. Verify secrets in GitHub Settings → Secrets
2. Test bot token: `https://api.telegram.org/bot<TOKEN>/getMe`
3. Ensure chat ID is correct (numeric value)

---

### **403 Forbidden Errors**

**Cause**: Job portals blocking GitHub Actions IP

**Solution**: 
- Indeed and Instahyre may block automated requests
- LinkedIn and Internshala usually work fine
- System continues with available portals

---

### **Dashboard Shows Old Data**

**Cause**: Streamlit cache (5-minute TTL)

**Solution**:
1. Wait 5 minutes for auto-refresh
2. Click "Rerun" button in dashboard
3. Press 'R' key to force refresh

---

## 🔬 Research Use Cases

This system generates publication-ready data for research:

### **Potential Research Questions**
1. **Job Market Analysis**: Trends in data analyst internship postings
2. **Skill Demand**: Most requested technical skills in job descriptions
3. **Portal Comparison**: Quality differences across job platforms
4. **Scoring Validation**: Comparing AI vs keyword-based matching
5. **Temporal Patterns**: When are most jobs posted?

### **Sample Research Metrics**
- Precision/Recall of filtering system
- False positive rate (keyword vs AI)
- Average time-to-fill for positions
- Skill requirement trends over time
- Portal-specific quality scores

---

## 🛠️ Tech Stack

- **Language**: Python 3.11
- **Automation**: GitHub Actions
- **Web Scraping**: BeautifulSoup4, Requests
- **Dashboard**: Streamlit, Plotly
- **Data Processing**: Pandas, CSV, JSON
- **Notifications**: Telegram Bot API
- **Scheduling**: Cron (GitHub Actions)
- **AI/ML**: Keyword-based semantic matching (no external models)

---

## 📝 Dependencies

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.3
python-telegram-bot>=20.0
streamlit>=1.31.0
plotly>=5.18.0
```

**Note**: No heavy ML dependencies (TensorFlow, PyTorch, sentence-transformers) required!

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more job portals (Glassdoor, Monster, etc.)
- [ ] Email notifications for high-scoring jobs
- [ ] Mobile app integration
- [ ] Advanced ML-based semantic matching
- [ ] Multi-user support with personalized profiles
- [ ] Customizable filtering rules per user
- [ ] Company reputation scoring
- [ ] Salary range prediction

---

## 📄 License

MIT License - feel free to use and modify for your needs!

---

## 🎯 Future Enhancements

### **Short-term**
- [ ] Add email alerts for 70%+ matches
- [ ] Export to Google Sheets integration
- [ ] Add more technical skills to detection
- [ ] Company size/reputation filtering

### **Medium-term**
- [ ] Dashboard user authentication
- [ ] Historical trend comparisons
- [ ] Job application tracking
- [ ] Interview preparation recommendations

### **Long-term**
- [ ] Advanced NLP with sentence-transformers
- [ ] Multi-language support
- [ ] Salary range prediction ML model
- [ ] Company culture analysis
- [ ] Career path recommendations

---

## 🙏 Acknowledgments

Built with:
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- [Streamlit](https://streamlit.io/) for dashboard
- [Plotly](https://plotly.com/) for interactive charts
- [Telegram Bot API](https://core.telegram.org/bots/api) for notifications
- [GitHub Actions](https://github.com/features/actions) for automation

---

## 📞 Support

**Issues?** Open an issue in this repository

**Questions?** Check the [Troubleshooting](#-troubleshooting) section

**Improvements?** Submit a pull request!

---

## ⭐ Star This Repository

If this project helped you land a job, give it a star! ⭐

---


**Made with ❤️ for data analysts seeking their dream internship**

**Last Updated**: February 2026

---

## 💼 About the Author

Built by a data analyst who needed a smarter way to track job opportunities. This project started as a simple scraper and evolved into a full AI-powered intelligence system.

---

**Start your job search journey today! Fork this repo and let AI find your perfect opportunity.** 🚀
