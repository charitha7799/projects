import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="Income vs Credit",
    page_icon="💰",
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

st.title("💰 Income vs Credit Analysis")
st.caption(
    "Understanding customer income, credit exposure and affordability"
)

st.divider()


# ---------------------------------------------------------
# CLEAN DATA FOR VISUALIZATION
# ---------------------------------------------------------

required_columns = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "TARGET"
]

plot_df = df[required_columns].copy()

plot_df = plot_df.dropna(
    subset=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET"
    ]
)

# Remove invalid / zero values
plot_df = plot_df[
    (plot_df["AMT_INCOME_TOTAL"] > 0) &
    (plot_df["AMT_CREDIT"] > 0) &
    (plot_df["AMT_ANNUITY"] > 0)
]

# Sample for faster visualization
sample = plot_df.sample(
    min(15000, len(plot_df)),
    random_state=42
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

avg_income = plot_df["AMT_INCOME_TOTAL"].mean()
avg_credit = plot_df["AMT_CREDIT"].mean()
avg_annuity = plot_df["AMT_ANNUITY"].mean()

credit_income = (
    plot_df["AMT_CREDIT"] /
    plot_df["AMT_INCOME_TOTAL"]
).mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Income",
    f"{avg_income:,.0f}"
)

c2.metric(
    "Average Credit",
    f"{avg_credit:,.0f}"
)

c3.metric(
    "Average Annuity",
    f"{avg_annuity:,.0f}"
)

c4.metric(
    "Avg Credit / Income",
    f"{credit_income:.2f}x"
)

st.divider()


# ---------------------------------------------------------
# INCOME VS CREDIT
# ---------------------------------------------------------

st.header("📈 Income vs Credit Exposure")

fig = px.scatter(
    sample,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET",
    size="AMT_ANNUITY",
    hover_data=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET"
    ],
    opacity=0.65,
    color_continuous_scale="Purples",
    size_max=25
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Customer Income",
    yaxis_title="Credit Amount",
    legend_title="Historical Default"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Business Insight**

    This chart compares how much customers earn against the amount of
    credit they receive.

    Larger bubbles represent higher annuity obligations.

    Customers with high credit and high repayment obligations compared
    with their income deserve closer affordability analysis.
    """
)


# ---------------------------------------------------------
# CREDIT / INCOME RATIO
# ---------------------------------------------------------

st.header("⚖️ Credit-to-Income Ratio")

plot_df["CREDIT_INCOME_RATIO"] = (
    plot_df["AMT_CREDIT"] /
    plot_df["AMT_INCOME_TOTAL"]
)

ratio = plot_df["CREDIT_INCOME_RATIO"].clip(
    upper=plot_df["CREDIT_INCOME_RATIO"].quantile(0.99)
)

fig = px.histogram(
    x=ratio,
    nbins=50,
    color_discrete_sequence=["#9C27B0"]
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Credit / Income Ratio",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Business Insight**

    The Credit-to-Income Ratio shows how large the requested credit is
    compared with customer income.

    A higher ratio indicates greater credit exposure relative to income.
    """
)


# ---------------------------------------------------------
# 3D ANALYSIS
# ---------------------------------------------------------

st.header("🌌 3D Income – Credit – Annuity Analysis")

three_d = sample.sample(
    min(6000, len(sample)),
    random_state=42
)

fig = px.scatter_3d(
    three_d,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    z="AMT_ANNUITY",
    color="TARGET",
    opacity=0.60,
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
    🧠 **3D Business Insight**

    This view combines three important financial dimensions:

    💰 Income → earning capacity

    💳 Credit → borrowing exposure

    💸 Annuity → repayment obligation

    Looking at all three together gives a more complete picture of
    customer affordability.
    """
)


# ---------------------------------------------------------
# FINAL BUSINESS INSIGHTS
# ---------------------------------------------------------

st.divider()

st.header("💼 Key Business Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        """
        **💰 Income**

        Higher income generally provides greater repayment capacity.
        """
    )

with col2:
    st.warning(
        """
        **💳 Credit Exposure**

        High credit relative to income can indicate increased financial
        exposure.
        """
    )

with col3:
    st.info(
        """
        **💸 Repayment Burden**

        Annuity should be evaluated together with income rather than
        independently.
        """
    )

st.success(
    """
    🎯 **Overall Business Conclusion**

    Income, credit amount and annuity should be analysed together when
    evaluating affordability and historical repayment behaviour.
    """
)