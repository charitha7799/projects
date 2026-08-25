import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Regional Risk",
    page_icon="🗺️",
    layout="wide"
)

df = preprocess_data(load_data())

st.title("🗺️ Regional Risk Analysis")
st.caption("Regional ratings and historical repayment behaviour")
st.divider()

rating = df["REGION_RATING_CLIENT"].value_counts().reset_index()
rating.columns = ["Region Rating", "Customers"]

st.header("📊 Regional Rating Distribution")

fig = px.bar(
    rating,
    x="Region Rating",
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
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Regional ratings show how customers are distributed
    across different regional classifications.
    """
)

st.header("🎯 Historical Default Rate")

risk = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

risk.columns = [
    "Region Rating",
    "Default Rate"
]

fig = px.bar(
    risk,
    x="Region Rating",
    y="Default Rate",
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
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Comparing default rates across regional ratings helps
    identify differences in historical portfolio behaviour.
    """
)

st.success(
    """
    💼 **Business Insight:** Regional analysis can support portfolio
    monitoring and help identify segments requiring further investigation.
    """
)