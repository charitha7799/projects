import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Annuity Analysis", page_icon="💵", layout="wide")

df = preprocess_data(load_data())

df["PAYMENT_BURDEN"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]

st.title("💵 Repayment Obligation Analysis")
st.caption("Annuity, affordability and repayment burden")
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("Average Annuity", f"{df.AMT_ANNUITY.mean():,.0f}")
c2.metric("Median Annuity", f"{df.AMT_ANNUITY.median():,.0f}")
c3.metric("Average Burden", f"{df.PAYMENT_BURDEN.mean()*100:.2f}%")

sample = df.sample(min(15000, len(df)), random_state=42)

st.header("📊 Annuity Distribution")

fig = px.histogram(
    sample,
    x="AMT_ANNUITY",
    color="TARGET",
    nbins=50,
    marginal="box",
    color_discrete_sequence=["#B388FF", "#5E35B1"]
)

fig.update_layout(template="plotly_dark", height=550)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** Annuity represents the recurring repayment obligation "
    "and is an important component of affordability analysis."
)

st.header("⚖️ Payment Burden by Risk")

fig = px.box(
    sample,
    x="TARGET",
    y="PAYMENT_BURDEN",
    color="TARGET",
    points=False,
    color_discrete_sequence=["#B388FF", "#5E35B1"]
)

fig.update_layout(template="plotly_dark", height=500)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** Payment burden compares annuity with income and "
    "helps identify customers facing relatively higher repayment pressure."
)

st.success(
    "💼 **Business Insight:** Repayment obligation should be evaluated "
    "against income rather than viewed as an isolated amount."
)