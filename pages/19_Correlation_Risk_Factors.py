import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Correlation Risk Factors",
    page_icon="🔥",
    layout="wide"
)

df = preprocess_data(load_data())

st.title("🔥 Correlational Risk Factors")
st.caption("Relationships between major financial and risk variables")
st.divider()

columns = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

available = [
    c for c in columns
    if c in df.columns
]

corr = df[available].corr()

st.header("🔥 Risk Factor Correlation Heatmap")

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="Purples",
    aspect="auto"
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
    🧠 **Insight:** The heatmap shows how strongly variables move
    together and helps identify relationships worth investigating.
    """
)

st.header("🎯 Correlation with Default Target")

target_corr = (
    corr["TARGET"]
    .drop("TARGET")
    .sort_values()
    .reset_index()
)

target_corr.columns = [
    "Risk Factor",
    "Correlation"
]

fig = px.bar(
    target_corr,
    x="Correlation",
    y="Risk Factor",
    orientation="h",
    color="Correlation",
    text="Correlation",
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Insight:** Variables with stronger relationships to TARGET can
    be investigated further as potential risk indicators. Correlation
    does not prove causation.
    """
)

st.header("🌐 Risk Factor Relationship Matrix")

sample = df.sample(
    min(5000, len(df)),
    random_state=42
)

dimensions = [
    c for c in [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "EXT_SOURCE_2"
    ]
    if c in df.columns
]

fig = px.scatter_matrix(
    sample,
    dimensions=dimensions,
    color="TARGET",
    color_continuous_scale="Purples",
    height=850
)

fig.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success(
    """
    💼 **Business Insight:** Correlation analysis helps identify useful
    variables for deeper feature engineering, modelling and risk analysis.
    """
)