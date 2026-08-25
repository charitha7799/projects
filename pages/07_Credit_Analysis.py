import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="Credit Analysis",
    page_icon="💳",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("💳 Credit Analysis")
st.caption(
    "Understanding credit exposure, loan amounts and historical repayment risk"
)

st.divider()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

avg_credit = df["AMT_CREDIT"].mean()
median_credit = df["AMT_CREDIT"].median()
max_credit = df["AMT_CREDIT"].max()
avg_goods = df["AMT_GOODS_PRICE"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Credit",
    f"{avg_credit:,.0f}"
)

c2.metric(
    "Median Credit",
    f"{median_credit:,.0f}"
)

c3.metric(
    "Maximum Credit",
    f"{max_credit:,.0f}"
)

c4.metric(
    "Avg Goods Price",
    f"{avg_goods:,.0f}"
)

st.divider()


# ---------------------------------------------------------
# CREDIT DISTRIBUTION
# ---------------------------------------------------------

st.header("📊 Credit Amount Distribution")

sample = df.sample(
    min(15000, len(df)),
    random_state=42
)

fig = px.histogram(
    sample,
    x="AMT_CREDIT",
    color="TARGET",
    nbins=50,
    marginal="box",
    color_discrete_sequence=[
        "#B388FF",
        "#6A1B9A"
    ]
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Credit Amount",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Business Insight:**  
    This chart shows how credit amounts are distributed across customers.
    Comparing default and non-default customers helps identify whether
    repayment difficulty is concentrated around particular credit levels.
    """
)


# ---------------------------------------------------------
# CREDIT VS GOODS PRICE
# ---------------------------------------------------------

st.header("💳 Credit Amount vs Goods Price")

fig = px.scatter(
    sample,
    x="AMT_GOODS_PRICE",
    y="AMT_CREDIT",
    color="TARGET",
    opacity=0.55,
    color_continuous_scale="Purples"
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Goods Price",
    yaxis_title="Credit Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Insight:**  
    The relationship between goods price and credit amount helps identify
    customers whose requested credit differs substantially from the
    underlying purchase value.
    """
)


# ---------------------------------------------------------
# 3D CREDIT ANALYSIS
# ---------------------------------------------------------

st.header("🌐 3D Credit Risk View")

three_d = sample.sample(
    min(7000, len(sample)),
    random_state=42
)

fig = px.scatter_3d(
    three_d,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    z="AMT_ANNUITY",
    color="TARGET",
    opacity=0.55,
    color_continuous_scale="Purples"
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    scene=dict(
        xaxis_title="Income",
        yaxis_title="Credit",
        zaxis_title="Annuity"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **3D Insight:**  
    Income, credit and annuity are viewed together to understand the
    customer's financial exposure rather than analysing one variable
    independently.
    """
)


# ---------------------------------------------------------
# BUSINESS INSIGHT
# ---------------------------------------------------------

st.divider()

st.header("💼 Credit Analysis — Business Insights")

st.success(
    """
    • Credit exposure should be evaluated against customer income.

    • High credit alone does not automatically indicate high risk.

    • Credit amount, goods price and annuity together provide a stronger
      affordability picture.

    • Customers showing unusually high exposure relative to income can
      be prioritised for deeper financial analysis.
    """
)