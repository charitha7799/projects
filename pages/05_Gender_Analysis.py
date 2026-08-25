import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


st.set_page_config(
    page_title="Gender Analysis",
    page_icon="👥",
    layout="wide"
)


df = load_data()
df = preprocess_data(df)


st.title("👥 Gender Risk Intelligence")

st.caption(
    "Customer distribution and historical repayment outcomes by gender"
)

st.divider()


# =========================================================
# GENDER COUNTS
# =========================================================

gender = (
    df["CODE_GENDER"]
    .value_counts()
    .reset_index()
)

gender.columns = [
    "Gender",
    "Customers"
]


c1, c2, c3 = st.columns(3)

for i, row in gender.iterrows():

    if i == 0:
        c1.metric(
            f"Gender {row['Gender']}",
            f"{row['Customers']:,}"
        )

    elif i == 1:
        c2.metric(
            f"Gender {row['Gender']}",
            f"{row['Customers']:,}"
        )


c3.metric(
    "Total Customers",
    f"{len(df):,}"
)


st.divider()


# =========================================================
# DONUT
# =========================================================

st.header("🍩 Gender Portfolio Distribution")

fig = px.pie(
    gender,
    names="Gender",
    values="Customers",
    hole=.58,
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
    🧠 **Insight:** The donut chart shows the relative contribution of
    each gender segment to the overall customer portfolio.
    """
)


# =========================================================
# DEFAULT RATE
# =========================================================

st.header("🎯 Historical Default Rate by Gender")

risk = (
    df.groupby("CODE_GENDER")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

risk.columns = [
    "Gender",
    "Default Rate"
]


fig = px.bar(
    risk,
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
    height=480,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** Default-rate comparison is more meaningful than raw
    customer counts because it accounts for the different sizes of the
    gender segments.
    """
)


# =========================================================
# GENDER × INCOME
# =========================================================

st.header("💰 Gender × Income Distribution")

sample = df.sample(
    min(15000, len(df)),
    random_state=42
)


fig = px.box(
    sample,
    x="CODE_GENDER",
    y="AMT_INCOME_TOTAL",
    color="CODE_GENDER",
    points=False,
    color_discrete_sequence=[
        "#B388FF",
        "#5E35B1"
    ]
)

fig.update_layout(
    height=550,
    template="plotly_dark",
    xaxis_title="Gender",
    yaxis_title="Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.info(
    """
    🧠 **Insight:** The box plot compares income distributions across
    gender groups and makes differences in spread and central tendency
    easier to identify.
    """
)


# =========================================================
# GENDER × CREDIT
# =========================================================

st.header("💳 Gender × Credit Exposure")

fig = px.violin(
    sample,
    x="CODE_GENDER",
    y="AMT_CREDIT",
    color="CODE_GENDER",
    box=True,
    points=False,
    color_discrete_sequence=[
        "#B388FF",
        "#5E35B1"
    ]
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
    🧠 **Insight:** Credit exposure distributions provide additional
    financial context when comparing customer segments.
    """
)


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.divider()

st.header("💼 Gender Analysis — Business Insights")

st.success(
    """
    👥 **Portfolio Composition:** Gender analysis identifies the size
    and structure of customer segments.

    🎯 **Risk Comparison:** Historical default rates provide a descriptive
    comparison between groups.

    💰 **Financial Context:** Income and credit distributions provide
    additional information about customer financial profiles.

    ⚠️ **Responsible Analytics:** Demographic variables should not be
    used as standalone lending decisions.
    """
)