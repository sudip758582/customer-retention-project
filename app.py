import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")

# ---------------- PREMIUM UI CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141e30, #243b55);
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
}

.stMetric {
    background: rgba(255, 255, 255, 0.08);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.stDataFrame {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

activity = st.sidebar.selectbox(
    "Customer Activity",
    ["All", "Active", "Inactive"]
)

if activity == "Active":
    df = df[df["IsActiveMember"] == 1]
elif activity == "Inactive":
    df = df[df["IsActiveMember"] == 0]

# ---------------- TITLE ----------------
st.title("📊 Customer Retention Dashboard")

st.markdown("Analyze churn behavior, identify high-risk customers, and improve retention strategies.")

st.markdown("---")

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

total_customers = len(df)
churn_rate = df["Exited"].mean()
avg_balance = df["Balance"].mean()

col1.metric("👥 Total Customers", total_customers)
col2.metric("📉 Churn Rate", f"{churn_rate:.2%}")
col3.metric("💰 Avg Balance", f"{avg_balance:,.0f}")

st.markdown("---")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Engagement vs Churn")
    engagement = df.groupby("IsActiveMember")["Exited"].mean()
    
    # ✅ FIXED (safe mapping)
    engagement.index = engagement.index.map({0: "Inactive", 1: "Active"})
    
    st.bar_chart(engagement)

with col2:
    st.subheader("📦 Products vs Churn")
    product = df.groupby("NumOfProducts")["Exited"].mean()
    st.line_chart(product)

st.markdown("---")

# ---------------- HIGH RISK ----------------
st.subheader("⚠️ High Value Customers at Risk")

high_risk = df[
    (df["Balance"] > avg_balance) &
    (df["IsActiveMember"] == 0)
]

col1, col2 = st.columns([1,2])

col1.metric("High Risk Customers", high_risk.shape[0])
col2.dataframe(high_risk.head())

st.markdown("---")

# ---------------- RETENTION SCORE ----------------
st.subheader("⭐ Retention Score")

def retention_score(row):
    score = 0
    if row["IsActiveMember"] == 1:
        score += 2
    if row["NumOfProducts"] > 2:
        score += 2
    if row["Balance"] > avg_balance:
        score += 1
    return score

df["RetentionScore"] = df.apply(retention_score, axis=1)

st.bar_chart(df["RetentionScore"].value_counts().sort_index())

st.markdown("---")

# ---------------- DATA ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

st.markdown("""
- Active customers show significantly lower churn rates  
- Customers with more products tend to stay longer  
- High-balance inactive customers are at highest risk  
- Retention score helps segment loyal vs risky users  
""")
