import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


st.set_page_config(
    page_title="Demographic Analysis",
    page_icon="👥",
    layout="wide"
)


# =========================================================
# DATA
# =========================================================

df = load_data()
df = preprocess_data(df)


# =========================================================
# HEADER
# =========================================================

st.title("👥 Demographic Intelligence")

st.caption(
    "Customer composition, lifestyle characteristics and historical risk"
)

st.divider()


# =========================================================
# KPI
# =========================================================

total_customers = len(df)

gender_count = df["CODE_GENDER"].nunique()

education_count = df["NAME_EDUCATION_TYPE"].nunique()

family_count = df["NAME_FAMILY_STATUS"].nunique()


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Gender Groups",
    gender_count
)

c3.metric(
    "Education Groups",
    education_count
)

c4.metric(
    "Family Groups",
    family_count
)


st.divider()


# =========================================================
# GENDER DISTRIBUTION
# =========================================================

st.header("👩‍💼 Gender Distribution")

gender = (
    df["CODE_GENDER"]
    .value_counts()
    .reset_index()
)

gender.columns = [
    "Gender",
    "Customers"
]


fig = px.pie(
    gender,
    names="Gender",
    values="Customers",
    hole=0.58,
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
    height=500,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** The gender distribution shows the composition of
    the customer portfolio and helps establish the size of each segment.
    """
)


# =========================================================
# EDUCATION TREEMAP
# =========================================================

st.header("🎓 Education Portfolio")

education = (
    df["NAME_EDUCATION_TYPE"]
    .value_counts()
    .reset_index()
)

education.columns = [
    "Education",
    "Customers"
]


fig = px.treemap(
    education,
    path=["Education"],
    values="Customers",
    color="Customers",
    color_continuous_scale="Purples"
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
    🧠 **Insight:** The treemap makes portfolio concentration immediately
    visible. Larger blocks represent education groups with more customers.
    """
)


# =========================================================
# FAMILY STATUS
# =========================================================

st.header("👨‍👩‍👧 Family Status")

family = (
    df["NAME_FAMILY_STATUS"]
    .value_counts()
    .reset_index()
)

family.columns = [
    "Family Status",
    "Customers"
]


fig = px.bar(
    family,
    x="Family Status",
    y="Customers",
    color="Customers",
    text="Customers",
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig.update_xaxes(
    tickangle=-30
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
    🧠 **Insight:** Family status shows the household composition of the
    portfolio and provides additional context for customer segmentation.
    """
)


# =========================================================
# FAMILY STATUS DEFAULT RATE
# =========================================================

st.header("🎯 Historical Risk by Family Status")

family_risk = (
    df.groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

family_risk.columns = [
    "Family Status",
    "Default Rate"
]


fig = px.bar(
    family_risk,
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
    height=550,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Historical default rates can vary between household
    segments. These differences are useful for analysis but should not
    be treated as standalone decision rules.
    """
)


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.divider()

st.header("💼 Demographic Business Insights")

st.success(
    """
    👥 **Portfolio Composition:** Demographic analysis identifies the
    dominant customer groups.

    🎓 **Customer Profile:** Education and family characteristics provide
    useful descriptive information about the applicant base.

    🎯 **Risk Segmentation:** Comparing historical default rates across
    demographic groups helps identify areas requiring deeper analysis.

    💡 **Best Practice:** Demographic information should be combined with
    financial affordability, credit exposure and external risk indicators.
    """
)