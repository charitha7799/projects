import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Employment Analysis", page_icon="💼", layout="wide")

df = preprocess_data(load_data())

df["EMPLOYMENT_YEARS"] = abs(df["DAYS_EMPLOYED"]) / 365

# Handle Home Credit anomaly
df.loc[
    df["DAYS_EMPLOYED"] > 100000,
    "EMPLOYMENT_YEARS"
] = None

st.title("💼 Employment Risk Analysis")
st.caption("Employment duration, income type and historical repayment patterns")
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Employment",
    f"{df.EMPLOYMENT_YEARS.mean():.1f} Years"
)

c2.metric(
    "Income Types",
    df["NAME_INCOME_TYPE"].nunique()
)

c3.metric(
    "Customers",
    f"{len(df):,}"
)

st.divider()

sample = df.sample(
    min(15000, len(df)),
    random_state=42
)

st.header("📊 Employment Duration")

fig = px.histogram(
    sample,
    x="EMPLOYMENT_YEARS",
    color="TARGET",
    nbins=40,
    marginal="box",
    color_discrete_sequence=[
        "#B388FF",
        "#6A1B9A"
    ]
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Employment Years",
    yaxis_title="Customers"
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Employment duration gives additional context about
    customer employment stability and earning history.
    """
)

st.header("💰 Income Type Distribution")

income = df["NAME_INCOME_TYPE"].value_counts().reset_index()
income.columns = ["Income Type", "Customers"]

fig = px.bar(
    income,
    x="Income Type",
    y="Customers",
    color="Customers",
    text="Customers",
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_tickangle=-30
)

st.plotly_chart(fig, use_container_width=True)

st.header("🎯 Employment / Income Type Risk")

risk = (
    df.groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values()
    .reset_index()
)

risk.columns = ["Income Type", "Default Rate"]

fig = px.bar(
    risk,
    x="Default Rate",
    y="Income Type",
    orientation="h",
    color="Default Rate",
    text="Default Rate",
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Income-type categories show differences in historical
    repayment behaviour and help describe the employment structure of the
    portfolio.
    """
)

st.success(
    """
    💼 **Business Insight:** Employment information becomes more valuable
    when analysed together with income, credit exposure and repayment burden.
    """
)