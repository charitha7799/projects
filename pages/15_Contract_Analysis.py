import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Contract Analysis", page_icon="📑", layout="wide")

df = preprocess_data(load_data())

st.title("📑 Contract Analysis")
st.caption("Credit product distribution and historical repayment behaviour")
st.divider()

contract = df["NAME_CONTRACT_TYPE"].value_counts().reset_index()
contract.columns = ["Contract Type", "Customers"]

st.header("🍩 Contract Portfolio")

fig = px.pie(
    contract,
    names="Contract Type",
    values="Customers",
    hole=.60,
    color_discrete_sequence=[
        "#7E57C2",
        "#B388FF",
        "#D1A3FF"
    ]
)

fig.update_traces(
    textinfo="percent+label"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Contract distribution shows which credit products
    dominate the customer portfolio.
    """
)

st.header("🎯 Default Rate by Contract Type")

risk = (
    df.groupby("NAME_CONTRACT_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

risk.columns = ["Contract Type", "Default Rate"]

fig = px.bar(
    risk,
    x="Contract Type",
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
    🧠 **Insight:** Historical repayment rates can be compared across
    different contract products.
    """
)

st.success(
    """
    💼 **Business Insight:** Product-level risk monitoring can help
    identify credit products requiring closer portfolio attention.
    """
)