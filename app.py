"""
AI Job Agent - Analytics Dashboard
Clean Streamlit App
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import re

# Page config
st.set_page_config(page_title="AI Job Agent Dashboard", layout="wide")

# Load data
@st.cache_data(ttl=300)
def load_data():
    path = Path("jobs_dataset.csv")

    if not path.exists():
        return pd.DataFrame()

    try:
        df = pd.read_csv(path, on_bad_lines="skip", engine="python")

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        for col in ["ai_score", "hybrid_score"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            else:
                df[col] = 0

        if "location" not in df.columns:
            df["location"] = ""

        return df

    except:
        return pd.DataFrame()


# Extract skills
def extract_skills(text):
    if pd.isna(text):
        return []

    text = str(text).lower()

    skills = {
        "Python": r"\bpython\b",
        "SQL": r"\bsql\b",
        "Excel": r"\bexcel\b",
        "Power BI": r"\bpower\s*bi\b",
        "Tableau": r"\btableau\b"
    }

    return [k for k, v in skills.items() if re.search(v, text)]


# Main app
def main():
    st.title("AI Job Agent Dashboard")

    df = load_data()

    if df.empty:
        st.warning("No data found. Wait for jobs_dataset.csv.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")

    min_score = st.sidebar.slider("Min AI Score", 0.0, 1.0, 0.0, 0.05)
    keyword = st.sidebar.text_input("Search")

    filtered = df[df["ai_score"] >= min_score]

    if keyword:
        filtered = filtered[
            filtered["title"].str.contains(keyword, case=False, na=False)
        ]

    # KPIs
    st.subheader("KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Jobs", len(filtered))

    avg_score = filtered["ai_score"].mean() if not filtered.empty else 0
    col2.metric("Avg AI Score", f"{avg_score:.2f}")

    skills = sum([extract_skills(t) for t in filtered["title"]], [])
    top_skill = max(set(skills), key=skills.count) if skills else "N/A"
    col3.metric("Top Skill", top_skill)

    # Chart
    st.subheader("Jobs by Source")

    if "source" in filtered.columns:
        src = filtered["source"].value_counts().reset_index()
        src.columns = ["Source", "Count"]

        fig = px.bar(src, x="Source", y="Count")
        st.plotly_chart(fig, use_container_width=True)

    # Table
    st.subheader("Jobs Data")

    st.dataframe(filtered, use_container_width=True)

    # Download
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "jobs.csv")

    st.caption(f"Updated: {datetime.now()}")


if __name__ == "__main__":
    main()
