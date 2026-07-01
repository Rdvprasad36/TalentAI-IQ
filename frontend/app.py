import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="TalentIQ AI",
    layout="wide"
)
# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title(" TalentIQ AI")

    st.markdown(
        "### Explainable AI Candidate Ranking"
    )

    st.divider()

    st.success("✔ Hybrid AI Scoring")

    st.success("✔ Semantic Skill Matching")

    st.success("✔ Career Intelligence")

    st.success("✔ Behavioral Analysis")

    st.success("✔ Honeypot Detection")

    st.success("✔ Explainable Recommendations")

    st.divider()

    st.subheader("Project")

    st.write(" Redrob AI Hiring Challenge")

    st.write(" CPU Only")

    st.write("JSONL Streaming")

    st.write(" Top 100 Ranking")

    st.divider()

    st.caption(
        "Built with Passion and love using Python, Streamlit & FastAPI"
    )

st.title("🤖 Redrob AI Recruiter Dashboard")

st.markdown("""
This dashboard showcases an AI-powered candidate ranking system built for the Redrob AI Hiring Challenge.

### Key Features

- ✅ Semantic Skill Matching
- ✅ Career Progression Analysis
- ✅ Behavioral Signal Evaluation
- ✅ Honeypot Candidate Detection
- ✅ Explainable AI Ranking
""")

df = pd.read_csv("submission.csv")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Candidates Ranked",
    len(df)
)

col2.metric(
    "Highest Score",
    round(df["score"].max(),2)
)

col3.metric(
    "Average Score",
    round(df["score"].mean(),2)
)

col4.metric(
    "Top Selected",
    100
)


st.subheader(" Top 10 Candidates")

st.dataframe(
    df.head(10),
    use_container_width=True
)
st.subheader(" Score Distribution")

fig = px.histogram(
    df,
    x="score",
    nbins=20,
    title="Candidate Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()
candidate = st.selectbox(
    "Select Candidate",
    df["candidate_id"]
)
row = df[df["candidate_id"] == candidate]
candidate_data = row.iloc[0]

st.divider()

st.subheader(" Candidate Profile")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Candidate ID",
        candidate_data["candidate_id"]
    )

    st.metric(
        "Final Score",
        candidate_data["score"]
    )
    progress = min(
    float(candidate_data["score"]),
    100,
) / 100

st.progress(progress)

with col2:

    st.metric(
        "Rank",
        int(candidate_data["rank"])
    )

st.divider()

st.subheader(" AI Recruiter Reasoning")

st.success(candidate_data["reasoning"])
st.subheader(" AI Recruiter Summary")

score = float(candidate_data["score"])

if score >= 90:
    summary = """
This candidate demonstrates exceptional alignment with the AI Engineer role.
Strong technical depth, excellent career trajectory, high recruiter engagement,
and relevant AI experience make this candidate highly recommended for interview.
"""

elif score >= 80:
    summary = """
This candidate is a strong fit for the position.
The profile shows good AI skills, relevant experience,
and positive behavioral signals.
"""

elif score >= 70:
    summary = """
This candidate satisfies many hiring requirements but has
some gaps in experience or skill coverage.
Suitable for further evaluation.
"""

else:
    summary = """
This candidate has limited alignment with the target AI role.
Additional screening is recommended before proceeding.
"""

st.info(summary)
score = float(candidate_data["score"])

if score >= 90:
    st.success("🌟 Excellent Match")

elif score >= 80:
    st.info("✅ Strong Match")

elif score >= 70:
    st.warning("⚠ Moderate Match")

else:
    st.error("❌ Weak Match")
    import plotly.graph_objects as go

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=float(candidate_data["score"]),
        title={"text":"AI Match Score"},
        gauge={
            "axis":{"range":[0,100]}
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("⚙️ AI Ranking Pipeline")

st.code("""
 Candidate JSONL Dataset
        │
        ▼
 Data Preprocessing
        │
        ▼
 Feature Engineering
        │
        ▼
 Semantic Skill Matching
        │
        ▼
 Career Analysis
        │
        ▼
 Behavioral Signal Analysis
        │
        ▼
Honeypot Detection
        │
        ▼
 Hybrid Weighted Scoring
        │
        ▼
 Top-100 Candidate Ranking
        │
        ▼
Recruiter Dashboard
""")
st.subheader(" Technologies Used")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("""
🐍 Python

⚡ FastAPI

🎨 Streamlit

📊 Pandas
""")

with c2:
    st.info("""
 Feature Engineering

 Semantic Matching

 Hybrid Scoring

 Top-K Ranking
""")

with c3:
    st.info("""
 JSONL Streaming

 Honeypot Detection

 Career Intelligence

 Explainable AI
""")
st.subheader(" Performance")

p1, p2, p3 = st.columns(3)

p1.metric(
    "Runtime",
    "< 10 sec"
)

p2.metric(
    "Memory",
    "< 2 GB"
)

p3.metric(
    "Execution",
    "CPU Only"
)
st.divider()

st.caption(
    "RDV Prasad 36 | Built for the Redrob AI Hiring Challenge 2026 | AI-Powered Candidate Ranking System"
)