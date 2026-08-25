import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


st.set_page_config(
    page_title="Annuity Burden",
    page_icon="⚖️",
    layout="wide"
)

df = preprocess_data(load_data())


df["ANNUITY_BURDEN"] = (
    df["AMT_ANNUITY"] /
    df["AMT_INCOME_TOTAL"]
)


st.title("⚖️ Annuity Burden Analysis")
st.caption(
    "Understanding repayment obligation relative to customer income"
)

st.divider()


# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Annuity",
    f"{df.AMT_ANNUITY.mean():,.0f}"
)

c2.metric(
    "Median Annuity",
    f"{df.AMT_ANNUITY.median():,.0f}"
)

c3.metric(
    "Average Burden",
    f"{df.ANNUITY_BURDEN.mean()*100:.2f}%"
)

c4.metric(
    "High Burden Customers",
    f"{(df.ANNUITY_BURDEN > .40).sum():,}"
)

st.divider()


# ---------------------------------------------------------
# BURDEN DISTRIBUTION
# ---------------------------------------------------------

st.header("📊 Annuity Burden Distribution")

burden = df["ANNUITY_BURDEN"].clip(
    upper=df["ANNUITY_BURDEN"].quantile(.99)
)

fig = px.histogram(
    x=burden,
    nbins=50,
    color_discrete_sequence=["#7E57C2"]
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Annuity / Income",
    yaxis_title="Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:**  
    The annuity burden represents the repayment obligation relative to
    income. Higher values indicate greater repayment pressure.
    """
)


# ---------------------------------------------------------
# BURDEN GROUP
# ---------------------------------------------------------

df["BURDEN_GROUP"] = pd.cut(
    df["ANNUITY_BURDEN"],
    bins=[
        -1,
        .10,
        .20,
        .30,
        .40,
        1,
        10
    ],
    labels=[
        "<10%",
        "10–20%",
        "20–30%",
        "30–40%",
        "40–100%",
        "100%+"
    ]
)

risk = (
    df.groupby(
        "BURDEN_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

risk.columns = [
    "Burden Group",
    "Default Rate"
]


st.header("🎯 Historical Default Rate by Burden")

fig = px.bar(
    risk,
    x="Burden Group",
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

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:**  
    Comparing default rates across repayment-burden groups helps identify
    whether higher repayment pressure is associated with greater historical
    payment difficulty.
    """
)


st.success(
    """
    💼 **Business Insight:**  
    Annuity burden is an important affordability indicator and should be
    considered together with income, credit amount and external risk scores.
    """
)