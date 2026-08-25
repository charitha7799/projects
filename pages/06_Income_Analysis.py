import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Income Analysis", page_icon="💰", layout="wide")

df = preprocess_data(load_data())

st.title("💰 Income Risk Intelligence")
st.caption("Income distribution, earning capacity and repayment outcomes")
st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Income", f"{df.AMT_INCOME_TOTAL.mean():,.0f}")
c2.metric("Median Income", f"{df.AMT_INCOME_TOTAL.median():,.0f}")
c3.metric("Minimum Income", f"{df.AMT_INCOME_TOTAL.min():,.0f}")
c4.metric("Maximum Income", f"{df.AMT_INCOME_TOTAL.max():,.0f}")

st.divider()

sample = df.sample(min(15000, len(df)), random_state=42)

st.header("📊 Income Distribution")

fig = px.histogram(
    sample,
    x="AMT_INCOME_TOTAL",
    color="TARGET",
    nbins=50,
    marginal="box",
    color_discrete_sequence=["#B388FF", "#5E35B1"]
)

fig.update_layout(template="plotly_dark", height=550)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** Income distribution shows the earning profile of applicants "
    "and allows repayment outcomes to be compared across income levels."
)

st.header("💼 Income Type Portfolio")

income_type = df["NAME_INCOME_TYPE"].value_counts().reset_index()
income_type.columns = ["Income Type", "Customers"]

fig = px.treemap(
    income_type,
    path=["Income Type"],
    values="Customers",
    color="Customers",
    color_continuous_scale="Purples"
)

fig.update_layout(template="plotly_dark", height=550)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** The treemap highlights the dominant income categories "
    "within the customer portfolio."
)

st.header("🎯 Default Rate by Income Type")

risk = df.groupby("NAME_INCOME_TYPE")["TARGET"].mean().mul(100).reset_index()
risk.columns = ["Income Type", "Default Rate"]

fig = px.bar(
    risk.sort_values("Default Rate"),
    x="Default Rate",
    y="Income Type",
    orientation="h",
    color="Default Rate",
    text="Default Rate",
    color_continuous_scale="Purples"
)

fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig.update_layout(template="plotly_dark", height=600)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** Comparing default rates across income categories "
    "helps identify segments with different historical repayment behavior."
)

st.divider()

st.header("💼 Business Insights")

st.success(
    "Income is a key affordability indicator. It should be evaluated together "
    "with credit amount, annuity and repayment burden rather than independently."
)