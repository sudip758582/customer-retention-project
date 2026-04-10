import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filter Customers")

activity = st.sidebar.selectbox(
    "Select Activity Status",
    ["All", "Active", "Inactive"]
)

if activity == "Active":
    df = df[df["IsActiveMember"] == 1]
elif activity == "Inactive":
    df = df[df["IsActiveMember"] == 0]

# ---------------- TITLE ----------------
st.title("📊 Customer Retention Dashboard")

# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Customers", len(df))

with col2:
    churn_rate = df["Exited"].mean()
    st.metric("Churn Rate", f"{churn_rate:.2%}")

# ---------------- CHARTS ----------------
st.subheader("📈 Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("Engagement vs Churn")
    engagement_churn = df.groupby("IsActiveMember")["Exited"].mean()
    st.bar_chart(engagement_churn)

with col2:
    st.write("Products vs Churn")
    product_churn = df.groupby("NumOfProducts")["Exited"].mean()
    st.line_chart(product_churn)

# ---------------- HIGH VALUE AT RISK ----------------
st.subheader("⚠️ High Value Customers at Risk")

avg_balance = df["Balance"].mean()

high_risk = df[
    (df["Balance"] > avg_balance) &
    (df["IsActiveMember"] == 0)
]

col1, col2 = st.columns(2)

with col1:
    st.metric("High Risk Customers", high_risk.shape[0])

with col2:
    st.dataframe(high_risk.head())

# ---------------- RETENTION SCORE ----------------
st.subheader("⭐ Retention Score Analysis")

def retention_score(row):
    score = 0
    if row["IsActiveMember"] == 1:
        score += 2
    if row["NumOfProducts"] > 2:
        score += 2
    if row["Balance"] > df["Balance"].mean():
        score += 1
    return score

df["RetentionScore"] = df.apply(retention_score, axis=1)

st.bar_chart(df["RetentionScore"].value_counts())

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

st.markdown("""
- Active customers have lower churn rates.
- Customers using more products are more loyal.
- High-balance inactive customers are at high risk.
- Retention score helps identify loyal vs risky customers.
""")