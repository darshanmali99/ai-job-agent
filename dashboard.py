"""
AI Job Agent - Analytics Dashboard
READ-ONLY MODE: Safely reads from jobs_dataset.csv
HANDLES MALFORMED DATA GRACEFULLY
"""

from collections import Counter
from datetime import datetime
from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AI Job Agent Dashboard", page_icon="🤖", layout="wide")


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    """Load jobs_dataset.csv safely and handle malformed rows gracefully."""
    csv_path = Path("jobs_dataset.csv")
    if not csv_path.exists():
        return pd.DataFrame()

    try:
        df = pd.read_csv(csv_path, on_bad_lines="skip", engine="python")

        required_cols = ["date", "title", "source", "link"]
        for col in required_cols:
            if col not in df.columns:
                st.error(f"Missing required column: {col}")
                return pd.DataFrame()

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        for col in ["ai_score", "keyword_score", "hybrid_score"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            else:
                df[col] = 0

        if "location" not in df.columns:
            df["location"] = ""

        return df

    except Exception as exc:
        st.error(f"CSV Parsing Error: {exc}")
        st.info(
            "💡 **Fix**: Go to your repository → Edit jobs_dataset.csv → Delete all content → "
            "Add header line → Commit"
        )
        st.code(
            "date,title,source,link,location,stipend_mentioned,easy_apply,"
            "ai_score,keyword_score,hybrid_score,keyword_pass,final_decision",
            language="csv",
        )
        return pd.DataFrame()


def extract_skills(text: str) -> list[str]:
    """Extract known skills from title text."""
    if pd.isna(text):
        return []

    text_lower = str(text).lower()
    skills = {
        "Python": r"\bpython\b",
        "SQL": r"\bsql\b",
        "Excel": r"\bexcel\b",
        "Power BI": r"\bpower\s*bi\b|\bpowerbi\b",
        "Tableau": r"\btableau\b",
        "Machine Learning": r"\bmachine\s*learning\b|\bml\b",
    }
    return [skill for skill, pattern in skills.items() if re.search(pattern, text_lower)]


def is_remote(row: pd.Series) -> bool:
    """Check if a job is remote based on title/location text."""
    text = f"{row.get('title', '')} {row.get('location', '')}".lower()
    return any(k in text for k in ["remote", "work from home", "wfh"])


def main() -> None:
    st.title("🤖 AI Job Agent Analytics Dashboard")
    st.markdown("**Research-Grade Intelligence** | Real-time job market insights")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data in jobs_dataset.csv")
        st.info(
            """💡 **Next Steps:**
1. Fix CSV format (see error above)
2. Or wait for GitHub Actions to populate fresh data
3. Refresh this page"""
        )
        st.stop()

    st.sidebar.header("🔍 Filters")
    min_ai_score = st.sidebar.slider("Min AI Score", 0.0, 1.0, 0.0, 0.05)

    if "date" in df.columns and not df["date"].isna().all():
        date_range = st.sidebar.date_input(
            "Date Range", value=(df["date"].min().date(), df["date"].max().date())
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range
    else:
        start_date = end_date = None

    sources = df["source"].dropna().unique().tolist() if "source" in df.columns else []
    selected_sources = st.sidebar.multiselect("Portals", sources, sources) if sources else []
    keyword = st.sidebar.text_input("🔎 Search", placeholder="Title or location...")

    filtered = df.copy()
    filtered = filtered[filtered["ai_score"] >= min_ai_score]

    if start_date and end_date and "date" in filtered.columns:
        date_values = filtered["date"].dt.date
        filtered = filtered[(date_values >= start_date) & (date_values <= end_date)]

    if selected_sources and "source" in filtered.columns:
        filtered = filtered[filtered["source"].isin(selected_sources)]

    if keyword:
        location_series = (
            filtered["location"] if "location" in filtered.columns else pd.Series("", index=filtered.index)
        )
        filtered = filtered[
            filtered["title"].str.contains(keyword, case=False, na=False)
            | location_series.str.contains(keyword, case=False, na=False)
        ]

    st.header("📊 KPIs")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Jobs", f"{len(filtered):,}")

    with col2:
        avg_score = filtered["ai_score"].mean() if "ai_score" in filtered.columns else 0
        st.metric("Avg AI Score", f"{avg_score:.1%}")

    with col3:
        all_skills = sum([extract_skills(row.get("title", "")) for _, row in filtered.iterrows()], [])
        if all_skills:
            top_skill, count = Counter(all_skills).most_common(1)[0]
            st.metric("Top Skill", top_skill, f"{count} jobs")
        else:
            st.metric("Top Skill", "N/A")

    with col4:
        remote_count = int(filtered.apply(is_remote, axis=1).sum()) if not filtered.empty else 0
        remote_pct = (remote_count / len(filtered) * 100) if len(filtered) > 0 else 0
        st.metric("Remote %", f"{remote_pct:.1f}%", f"{remote_count} jobs")

    st.header("📈 Analytics")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Daily Trend")
        if "date" in filtered.columns and not filtered["date"].isna().all():
            daily = filtered.groupby(filtered["date"].dt.date).size().reset_index(name="Count")
            daily.columns = ["Date", "Count"]
            fig = px.line(daily, x="Date", y="Count", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No date data")

    with col2:
        st.subheader("🎯 By Source")
        if "source" in filtered.columns:
            source_df = filtered["source"].value_counts().reset_index()
            source_df.columns = ["Source", "Count"]
            fig = px.pie(source_df, values="Count", names="Source", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No source data")

    st.subheader("💻 Skill Demand")
    skill_names = ["Python", "SQL", "Excel", "Power BI", "Tableau", "Machine Learning"]
    skill_count = {s: filtered["title"].str.contains(s, case=False, na=False).sum() for s in skill_names}
    skill_count = {k: v for k, v in skill_count.items() if v > 0}

    if skill_count:
        skill_df = pd.DataFrame(
            {"Skill": list(skill_count.keys()), "Jobs": list(skill_count.values())}
        ).sort_values("Jobs", ascending=True)
        fig = px.bar(skill_df, x="Jobs", y="Skill", orientation="h", text="Jobs")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills found")

    st.header("📋 Jobs")
    if not filtered.empty:
        cols = [
            c
            for c in ["date", "title", "source", "location", "ai_score", "hybrid_score", "link"]
            if c in filtered.columns
        ]
        display = filtered[cols].copy()

        st.dataframe(
            display,
            column_config={
                "link": st.column_config.LinkColumn("Link", display_text="Apply →"),
                "ai_score": st.column_config.ProgressColumn(
                    "AI", format="%.0f%%", min_value=0, max_value=1
                ),
                "hybrid_score": st.column_config.ProgressColumn(
                    "Hybrid", format="%.0f%%", min_value=0, max_value=1
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        st.subheader("💾 Export")
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download CSV",
            csv_bytes,
            f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv",
        )
    else:
        st.warning("No jobs match filters")

    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total: {len(df):,}")


if __name__ == "__main__":
    main()
