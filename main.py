import streamlit as st
import pandas as pd
import os
import re
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="LeadRevive AI", layout="wide")

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1, h2, h3, h4 {
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.stMetric {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
div.stButton > button {
    background-color: #6366f1;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.title("🚀 LeadRevive AI")
st.markdown("### AI-Powered Revenue Intelligence System")
st.markdown("Automatically analyze, prioritize, and forecast revenue from incoming leads using intelligent scoring models.")

st.markdown("---")

# ---------- VALIDATION ----------
def valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# ---------- SMART SCORING ----------
def calculate_score(budget, urgency):

    # Budget weight (0–60)
    if budget >= 100000:
        budget_score = 60
    elif budget >= 50000:
        budget_score = 45
    elif budget >= 20000:
        budget_score = 30
    elif budget > 0:
        budget_score = 15
    else:
        budget_score = 0

    # Urgency weight (0–40)
    urgency_map = {
        "High": 40,
        "Medium": 25,
        "Low": 10
    }

    urgency_score = urgency_map.get(urgency, 0)

    return budget_score + urgency_score

def classify_lead(score):
    if score >= 80:
        return "Hot"
    elif score >= 50:
        return "Warm"
    else:
        return "Cold"

# ---------- MAIN LAYOUT ----------
left, right = st.columns([1, 1])

with left:
    st.subheader("📥 Capture New Lead")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    budget = st.number_input("Expected Budget (₹)", min_value=0)
    urgency = st.selectbox("Buying Intent", ["Low", "Medium", "High"])

    analyze = st.button("Analyze Lead")

with right:
    st.subheader("🧠 AI Intelligence Engine")

# ---------- PROCESS ----------
if analyze:

    if not name:
        st.error("Name is required")
        st.stop()

    if not valid_email(email):
        st.error("Invalid email format")
        st.stop()

    if not valid_phone(phone):
        st.error("Phone number must be 10 digits")
        st.stop()

    score = calculate_score(budget, urgency)
    classification = classify_lead(score)

    # Duplicate detection
    if os.path.exists("leads.csv"):
        existing_df = pd.read_csv("leads.csv")
        if email in existing_df["Email"].values:
            right.warning("⚠ Lead already exists. Updating record.")

    # Display result
    if classification == "Hot":
        right.error(f"🔥 High Priority Lead | Score: {score}/100")
    elif classification == "Warm":
        right.warning(f"🟡 Moderate Priority Lead | Score: {score}/100")
    else:
        right.info(f"🔵 Low Priority Lead | Score: {score}/100")

    right.success("✔ Lead processed and routed to sales pipeline.")

    # Decision Breakdown
    right.markdown("### 🔎 AI Decision Breakdown")
    right.write(f"- Budget entered: ₹{budget}")
    right.write(f"- Buying Intent: {urgency}")
    right.write(f"- Final Weighted Score: {score}/100")
    right.write(f"- Classified as: {classification}")

    # Save Data
    data = {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Budget": budget,
        "Urgency": urgency,
        "Lead Score": classification,
        "Numeric Score": score,
        "Timestamp": datetime.now()
    }

    new_df = pd.DataFrame([data])

    if os.path.exists("leads.csv"):
        existing = pd.read_csv("leads.csv")
        existing = existing[existing["Email"] != email]
        new_df = pd.concat([existing, new_df], ignore_index=True)

    new_df.to_csv("leads.csv", index=False)

# ---------- DASHBOARD ----------
st.markdown("---")
st.header("📊 Revenue Intelligence Dashboard")

if os.path.exists("leads.csv"):

    df = pd.read_csv("leads.csv")
    df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")

    total_leads = len(df)
    total_revenue = int(df["Budget"].sum())
    hot_leads = len(df[df["Lead Score"] == "Hot"])
    conversion_rate = round((hot_leads / total_leads) * 100, 1) if total_leads > 0 else 0

    projected_revenue = int(df[df["Lead Score"] == "Hot"]["Budget"].sum() * 0.3)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Leads", total_leads)
    col2.metric("Hot Leads", hot_leads)
    col3.metric("Conversion Rate (%)", conversion_rate)
    col4.metric("Projected Revenue (₹)", projected_revenue)

    # ---------- SMALL STATIC BAR GRAPH ----------
    st.markdown("### 📊 Lead Quality Distribution")

    lead_counts = df["Lead Score"].value_counts().reindex(["Hot", "Warm", "Cold"]).fillna(0)

    fig = px.bar(
        x=lead_counts.index,
        y=lead_counts.values,
        labels={"x": "Lead Category", "y": "Leads"},
        text=lead_counts.values,
        height=300
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="white",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    fig.update_traces(
        textposition="outside",
        marker_color="#6366f1"
    )

    st.plotly_chart(
        fig,
        use_container_width=False,
        config={"displayModeBar": False}
    )

    st.markdown("### 📋 Lead Database")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No leads captured yet.")

# ---------- WORKFLOW ----------
st.markdown("---")

with st.expander("⚙️ View AI Agent Workflow"):
    st.markdown("""
    1. Capture Lead Inquiry  
    2. Validate Contact Information  
    3. Apply Weighted AI Scoring Model  
    4. Classify Revenue Potential  
    5. Store & Update Database  
    6. Generate Revenue Forecast  
    """)