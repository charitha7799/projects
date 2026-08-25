import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Educational Analysis", page_icon="🎓", layout="wide")

df = preprocess_data(load_data())

st.title("🎓 Educational Risk Analysis")
st.caption("Education profile and historical repayment behaviour")
st.divider()

education = df["NAME_EDUCATION_TYPE"].value_counts().reset_index()
education.columns = ["Education", "Customers"]

c1, c2, c3 = st.columns(3)

c1.metric("Education Groups", df["NAME_EDUCATION_TYPE"].nunique())
c2.metric("Largest Group", education.iloc[0]["Education"])
c3.metric("Customers", f"{len(df):,}")

st.divider()

st.header("🌳 Education Portfolio")

fig = px.treemap(
    education,
    path=["Education"],
    values="Customers",
    color="Customers",
    color_continuous_scale="Purples"
)

fig.update_layout(template="plotly_dark", height=600)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "🧠 **Insight:** The treemap clearly shows which education categories "
    "represent the largest portions of the customer portfolio."
)

st.header("🎯 Default Rate by Education")

risk = (
    df.groupby("NAME_EDUCATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values()
    .reset_index()
)

risk.columns = ["Education", "Default Rate"]

fig = px.bar(
    risk,
    x="Default Rate",
    y="Education",
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
    "🧠 **Insight:** Historical default rates can vary across education "
    "groups. This helps identify segments that deserve deeper analysis."
)

st.success(
    """
    💼 **Business Insight:** Education provides useful customer context,
    but should not be used as an independent lending decision factor.
    """
)