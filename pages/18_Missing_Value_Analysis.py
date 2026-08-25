import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.set_page_config(
    page_title="Missing Value Analysis",
    page_icon="🔍",
    layout="wide"
)

df = load_data()

st.title("🔍 Missing Value Analysis")
st.caption("Data completeness and quality assessment")
st.divider()

total_missing = int(df.isnull().sum().sum())

affected_columns = int(
    df.isnull().any().sum()
)

missing_percentage = (
    total_missing /
    (df.shape[0] * df.shape[1])
) * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", f"{df.shape[1]:,}")
c3.metric("Missing Values", f"{total_missing:,}")
c4.metric("Missing %", f"{missing_percentage:.2f}%")

st.divider()

missing = (
    df.isnull()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0].head(30).reset_index()

missing.columns = [
    "Column",
    "Missing Values"
]

st.header("📊 Top Missing-Value Columns")

fig = px.bar(
    missing,
    x="Missing Values",
    y="Column",
    orientation="h",
    color="Missing Values",
    text="Missing Values",
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Insight:** Missing-value analysis identifies columns that require
    preprocessing before they can be reliably used for analytics or modelling.
    """
)

st.header("📋 Missing Value Summary")

summary = df.isnull().sum().reset_index()

summary.columns = [
    "Column",
    "Missing Values"
]

summary["Missing %"] = (
    summary["Missing Values"] /
    len(df) * 100
).round(2)

st.dataframe(
    summary.sort_values(
        "Missing Values",
        ascending=False
    ),
    use_container_width=True
)

st.success(
    """
    💼 **Business Insight:** Better data quality improves the reliability
    of dashboards, statistical analysis and machine-learning predictions.
    """
)

