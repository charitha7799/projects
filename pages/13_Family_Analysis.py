import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Family Analysis", page_icon="👨‍👩‍👧", layout="wide")

df = preprocess_data(load_data())

st.title("👨‍👩‍👧 Family Risk Analysis")
st.caption("Household structure and historical repayment behaviour")
st.divider()

family = df["NAME_FAMILY_STATUS"].value_counts().reset_index()
family.columns = ["Family Status", "Customers"]

c1, c2, c3 = st.columns(3)

c1.metric("Family Groups", df["NAME_FAMILY_STATUS"].nunique())
c2.metric("Largest Group", family.iloc[0]["Family Status"])
c3.metric("Customers", f"{len(df):,}")

st.divider()

st.header("🌳 Family Status Portfolio")

fig = px.treemap(
    family,
    path=["Family Status"],
    values="Customers",
    color="Customers",
    color_continuous_scale="Purples"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** The treemap highlights the dominant household "
    "categories in the customer portfolio."
)

st.header("🎯 Default Rate by Family Status")

risk = (
    df.groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

risk.columns = ["Family Status", "Default Rate"]

fig = px.bar(
    risk,
    x="Default Rate",
    y="Family Status",
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
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Comparing historical default rates between household
    groups helps identify differences in repayment patterns.
    """
)

st.success(
    """
    💼 **Business Insight:** Household structure provides useful descriptive
    context but should be combined with financial affordability indicators.
    """
)