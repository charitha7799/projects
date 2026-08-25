import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


st.set_page_config(
    page_title="Age Analysis",
    page_icon="🎂",
    layout="wide"
)


df = load_data()
df = preprocess_data(df)


# =========================================================
# AGE FEATURE
# =========================================================

df["AGE"] = abs(df["DAYS_BIRTH"]) / 365


# =========================================================
# HEADER
# =========================================================

st.title("🎂 Age Risk Intelligence")

st.caption(
    "Age distribution, customer segmentation and historical repayment behavior"
)

st.divider()


# =========================================================
# KPI
# =========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Age",
    f"{df['AGE'].mean():.1f} Years"
)

c2.metric(
    "Median Age",
    f"{df['AGE'].median():.1f} Years"
)

c3.metric(
    "Youngest",
    f"{df['AGE'].min():.0f} Years"
)

c4.metric(
    "Oldest",
    f"{df['AGE'].max():.0f} Years"
)


st.divider()


# =========================================================
# AGE DISTRIBUTION
# =========================================================

st.header("📊 Customer Age Distribution")

sample = df.sample(
    min(15000, len(df)),
    random_state=42
)


fig = px.histogram(
    sample,
    x="AGE",
    color="TARGET",
    nbins=45,
    marginal="box",
    color_discrete_sequence=[
        "#B388FF",
        "#5E35B1"
    ]
)

fig.update_layout(
    height=550,
    template="plotly_dark",
    xaxis_title="Age",
    yaxis_title="Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** The age distribution shows where the majority of
    applicants are concentrated and how historical repayment outcomes
    are distributed across ages.
    """
)


# =========================================================
# AGE GROUPS
# =========================================================

st.header("👥 Age Segmentation")

df["AGE_GROUP"] = pd.cut(
    df["AGE"],
    bins=[
        0,
        25,
        35,
        45,
        55,
        65,
        100
    ],
    labels=[
        "<25",
        "25–35",
        "35–45",
        "45–55",
        "55–65",
        "65+"
    ]
)


age_groups = (
    df["AGE_GROUP"]
    .value_counts()
    .sort_index()
    .reset_index()
)

age_groups.columns = [
    "Age Group",
    "Customers"
]


fig = px.bar(
    age_groups,
    x="Age Group",
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
    height=500,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Age grouping makes it easier to compare portfolio
    size across different customer life stages.
    """
)


# =========================================================
# DEFAULT RATE BY AGE
# =========================================================

st.header("🎯 Default Rate by Age Group")

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
    height=500,
    template="plotly_dark",
    yaxis_title="Historical Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Comparing age-group default rates against the overall
    portfolio baseline helps identify segments with relatively higher or
    lower historical repayment difficulty.
    """
)


# =========================================================
# AGE VS INCOME
# =========================================================

st.header("🌐 Age × Income × Risk")

fig = px.scatter(
    sample,
    x="AGE",
    y="AMT_INCOME_TOTAL",
    color="TARGET",
    size="AMT_CREDIT",
    opacity=0.55,
    color_continuous_scale="Purples"
)

fig.update_layout(
    height=600,
    template="plotly_dark",
    xaxis_title="Age",
    yaxis_title="Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** This multivariable view combines age, income and
    credit exposure, making it easier to explore customer financial
    patterns rather than looking at age alone.
    """
)


# =========================================================
# FINAL BUSINESS INSIGHT
# =========================================================

st.divider()

st.header("💼 Age Analysis — Business Insights")

st.success(
    """
    🎂 **Customer Segmentation:** Age provides a useful way to organize
    the customer portfolio into understandable life-stage groups.

    🎯 **Risk Monitoring:** Age-group default rates can be compared with
    the overall portfolio baseline.

    💰 **Affordability Context:** Combining age with income and credit
    exposure gives a stronger customer profile.

    💡 **Decision Support:** Age should be used as analytical context
    alongside financial and credit variables rather than independently.
    """
)