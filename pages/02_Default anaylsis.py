import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


st.set_page_config(
    page_title="Default Analysis",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

df = load_data()
df = preprocess_data(df)


# =========================================================
# HEADER
# =========================================================

st.title("🎯 Default Risk Analysis")

st.caption(
    "Understanding historical repayment difficulty across the portfolio"
)

st.divider()


# =========================================================
# KPI CARDS
# =========================================================

total = len(df)

default_cases = int(
    (df["TARGET"] == 1).sum()
)

non_default_cases = int(
    (df["TARGET"] == 0).sum()
)

default_rate = (
    default_cases / total
) * 100


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Applications",
    f"{total:,}"
)

c2.metric(
    "Payment Difficulty",
    f"{default_cases:,}"
)

c3.metric(
    "No Payment Difficulty",
    f"{non_default_cases:,}"
)

c4.metric(
    "Default Rate",
    f"{default_rate:.2f}%"
)


st.divider()


# =========================================================
# DONUT CHART
# =========================================================

st.header("🍩 Overall Risk Distribution")

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
    hole=0.60,
    color_discrete_sequence=[
        "#7E57C2",
        "#D1A3FF"
    ]
)

fig.update_traces(
    textinfo="percent+label",
    pull=[0, 0.08]
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    title="Historical Repayment Outcome"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    f"""
    🧠 **Insight:** Out of **{total:,} applications**, 
    **{default_cases:,}** have historical payment difficulty.
    The portfolio default rate is **{default_rate:.2f}%**.
    """
)


# =========================================================
# DEFAULT COUNT
# =========================================================

st.header("📊 Default Case Comparison")

fig = px.bar(
    risk,
    x="Status",
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
    height=480,
    template="plotly_dark",
    xaxis_title="Repayment Outcome",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** The portfolio is highly concentrated in the
    non-default category. Because default cases are the minority,
    percentage-based comparisons are important when evaluating segments.
    """
)


# =========================================================
# GENDER DEFAULT RATE
# =========================================================

st.header("👥 Default Rate by Gender")

gender = (
    df.groupby("CODE_GENDER")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

gender.columns = [
    "Gender",
    "Default Rate"
]


fig = px.bar(
    gender,
    x="Gender",
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
    height=450,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Gender-level default rates allow historical repayment
    outcomes to be compared across portfolio segments. This should be
    treated as descriptive analysis rather than a standalone lending rule.
    """
)


# =========================================================
# EDUCATION DEFAULT RATE
# =========================================================

st.header("🎓 Default Rate by Education")

education = (
    df.groupby("NAME_EDUCATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=True)
    .reset_index()
)

education.columns = [
    "Education",
    "Default Rate"
]


fig = px.bar(
    education,
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
    height=550,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Education categories show different historical
    repayment patterns. Comparing these rates with the overall portfolio
    baseline helps identify segments for further investigation.
    """
)


# =========================================================
# INCOME TYPE
# =========================================================

st.header("💼 Default Rate by Income Type")

income = (
    df.groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=True)
    .reset_index()
)

income.columns = [
    "Income Type",
    "Default Rate"
]


fig = px.bar(
    income,
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
    height=600,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Income-type segmentation highlights differences
    in historical repayment outcomes between employment and income groups.
    """
)


# =========================================================
# FINAL BUSINESS INSIGHT
# =========================================================

st.divider()

st.header("💼 Business Insights")

st.success(
    """
    🎯 **Risk Baseline:** The overall default rate provides the benchmark
    for evaluating all other customer segments.

    👥 **Customer Segmentation:** Gender, education and income type show
    differences in historical repayment behavior.

    📊 **Risk Monitoring:** Segment-level default rates are more useful
    than simply comparing the number of applications.

    💰 **Business Action:** Higher-risk segments should receive deeper
    affordability and financial-profile analysis rather than automatic
    rejection.
    """
)