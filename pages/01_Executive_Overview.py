import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Executive Overview",
    layout="wide"
)


# =========================================================
# DATA
# =========================================================

df = load_data()

df = preprocess_data(df)


# =========================================================
# FEATURES
# =========================================================

df["AGE"] = abs(df["DAYS_BIRTH"]) / 365

df["PAYMENT_BURDEN"] = (
    df["AMT_ANNUITY"]
    / df["AMT_INCOME_TOTAL"]
)


# =========================================================
# HEADER
# =========================================================

st.title(" Executive Risk Overview")

st.caption(
    "Portfolio performance • Financial exposure • Customer risk"
)

st.divider()


# =========================================================
# KPI
# =========================================================

total = len(df)

default_cases = int(
    (df["TARGET"] == 1).sum()
)

default_rate = (
    default_cases / total
) * 100

average_income = (
    df["AMT_INCOME_TOTAL"].mean()
)

average_credit = (
    df["AMT_CREDIT"].mean()
)

average_annuity = (
    df["AMT_ANNUITY"].mean()
)


c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "Applications",
    f"{total:,}"
)

c2.metric(
    "Default Rate",
    f"{default_rate:.2f}%"
)

c3.metric(
    "Default Cases",
    f"{default_cases:,}"
)

c4.metric(
    "Average Income",
    f"{average_income:,.0f}"
)

c5.metric(
    "Average Credit",
    f"{average_credit:,.0f}"
)


st.divider()


# =========================================================
# RISK DONUT
# =========================================================

st.header("🎯 Portfolio Risk Distribution")

risk = (
    df["TARGET"]
    .value_counts()
    .reset_index()
)

risk.columns = [
    "Target",
    "Customers"
]

risk["Status"] = risk["Target"].map(
    {
        0: "No Payment Difficulty",
        1: "Payment Difficulty"
    }
)


fig = px.pie(
    risk,
    names="Status",
    values="Customers",
    hole=0.62,
    color_discrete_sequence=[
        "#7E57C2",
        "#D1A3FF"
    ]
)

fig.update_layout(
    height=480,
    template="plotly_dark"
)

fig.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    f"""
    🧠 **Insight:** The portfolio contains **{total:,} applications**
    and the historical payment-difficulty rate is **{default_rate:.2f}%**.
    This rate provides the baseline against which individual customer
    segments can be compared.
    """
)


# =========================================================
# 3D FINANCIAL VIEW
# =========================================================

st.header("🌐 3D Financial Exposure")

sample = df.sample(
    min(7000, len(df)),
    random_state=42
)


fig = px.scatter_3d(
    sample,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    z="AMT_ANNUITY",
    color="TARGET",
    size="AMT_ANNUITY",
    opacity=0.6,
    color_continuous_scale="Purples"
)

fig.update_layout(
    height=680,
    template="plotly_dark",
    scene=dict(
        xaxis_title="Customer Income",
        yaxis_title="Credit Amount",
        zaxis_title="Annuity"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** This 3D visualization combines income, requested
    credit and repayment obligation. It helps identify customers whose
    credit exposure and repayment commitments are large relative to
    their income.
    """
)


# =========================================================
# CREDIT DISTRIBUTION
# =========================================================

st.header("💳 Credit Exposure Distribution")

fig = px.histogram(
    sample,
    x="AMT_CREDIT",
    color="TARGET",
    nbins=50,
    marginal="box",
    color_discrete_sequence=[
        "#B388FF",
        "#5E35B1"
    ]
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Credit Amount",
    yaxis_title="Applications"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** The distribution shows where loan requests are
    concentrated and allows repayment outcomes to be compared across
    different credit amounts.
    """
)


# =========================================================
# AGE RISK
# =========================================================

st.header("🎂 Age-Based Risk")

df["AGE_GROUP"] = pd.cut(
    df["AGE"],
    bins=[
        0,
        25,
        35,
        45,
        55,
        100
    ],
    labels=[
        "<25",
        "25–35",
        "35–45",
        "45–55",
        "55+"
    ]
)


age_risk = (
    df.groupby(
        "AGE_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

age_risk.columns = [
    "Age Group",
    "Default Rate"
]


fig = px.bar(
    age_risk,
    x="Age Group",
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
    height=480,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Age segmentation helps identify differences in
    historical repayment outcomes across customer life stages.
    """
)


# =========================================================
# PAYMENT BURDEN
# =========================================================

st.header("⚖️ Payment Burden")

fig = px.box(
    sample,
    x="TARGET",
    y="PAYMENT_BURDEN",
    color="TARGET",
    points=False,
    color_discrete_sequence=[
        "#B388FF",
        "#5E35B1"
    ]
)

fig.update_layout(
    height=480,
    template="plotly_dark",
    xaxis_title="Historical Outcome",
    yaxis_title="Annuity / Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Payment burden compares recurring repayment
    obligations with income, providing an important affordability
    perspective for customer risk analysis.
    """
)


# =========================================================
# FINAL INSIGHTS
# =========================================================

st.divider()

st.header("💼 Executive Business Insights")

st.success(
    """
    **1. Portfolio Risk:** The historical default rate provides the
    baseline risk level for evaluating customer segments.

    **2. Financial Exposure:** Income, credit amount and annuity should
    be considered together to understand affordability.

    **3. Customer Segmentation:** Age and other demographic variables
    reveal differences in historical repayment behavior.

    **4. Risk Monitoring:** Customers with high financial obligations
    relative to income deserve deeper affordability analysis.

    **5. Decision Support:** Multiple variables should be combined rather
    than relying on one indicator for credit-risk assessment.
    """
)