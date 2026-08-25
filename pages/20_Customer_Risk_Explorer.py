import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Customer Risk Explorer",
    page_icon="🔎",
    layout="wide"
)

df = preprocess_data(load_data())

st.title("🔎 Customer Risk Explorer")
st.caption(
    "Interactive customer-level financial and historical risk profile"
)

st.divider()


# ---------------------------------------------------------
# CUSTOMER SELECTION
# ---------------------------------------------------------

customer_index = st.number_input(
    "🔢 Select Customer Index",
    min_value=0,
    max_value=len(df) - 1,
    value=0,
    step=1
)

customer = df.iloc[int(customer_index)]


# ---------------------------------------------------------
# RISK STATUS
# ---------------------------------------------------------

if customer["TARGET"] == 1:

    st.error(
        "⚠️ Historical Payment Difficulty"
    )

    status = "Payment Difficulty"

else:

    st.success(
        "✅ No Historical Payment Difficulty"
    )

    status = "No Payment Difficulty"


st.divider()


# ---------------------------------------------------------
# CUSTOMER KPIs
# ---------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Income",
    f"{customer['AMT_INCOME_TOTAL']:,.0f}"
)

c2.metric(
    "Credit",
    f"{customer['AMT_CREDIT']:,.0f}"
)

c3.metric(
    "Annuity",
    f"{customer['AMT_ANNUITY']:,.0f}"
)

c4.metric(
    "Goods Price",
    f"{customer['AMT_GOODS_PRICE']:,.0f}"
)

st.divider()


# ---------------------------------------------------------
# FINANCIAL PROFILE
# ---------------------------------------------------------

st.header("💰 Customer Financial Profile")

financial = {
    "Income": customer["AMT_INCOME_TOTAL"],
    "Credit": customer["AMT_CREDIT"],
    "Annuity": customer["AMT_ANNUITY"],
    "Goods Price": customer["AMT_GOODS_PRICE"]
}

fig = px.bar(
    x=list(financial.keys()),
    y=list(financial.values()),
    color=list(financial.values()),
    text=list(financial.values()),
    color_continuous_scale="Purples"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Financial Metric",
    yaxis_title="Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    🧠 **Insight:** The financial profile gives a quick view of the
    selected customer's income, credit exposure, annuity and purchase value.
    """
)


# ---------------------------------------------------------
# CUSTOMER INFORMATION
# ---------------------------------------------------------

st.header("👤 Customer Profile")

profile_columns = [
    "CODE_GENDER",
    "NAME_FAMILY_STATUS",
    "NAME_EDUCATION_TYPE",
    "NAME_INCOME_TYPE",
    "NAME_HOUSING_TYPE",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY"
]

profile = {}

for column in profile_columns:

    if column in df.columns:

        profile[column] = customer[column]

st.dataframe(
    profile,
    use_container_width=True
)


# ---------------------------------------------------------
# EXTERNAL SCORES
# ---------------------------------------------------------

score_columns = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

available_scores = [
    c for c in score_columns
    if c in df.columns
]

if available_scores:

    st.header("📊 External Risk Scores")

    score_values = {
        c: customer[c]
        for c in available_scores
    }

    fig = px.bar(
        x=list(score_values.keys()),
        y=list(score_values.values()),
        color=list(score_values.values()),
        text=list(score_values.values()),
        color_continuous_scale="Purples"
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
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
        🧠 **Insight:** External scores provide additional risk context
        for the selected customer and should be interpreted alongside
        financial indicators.
        """)


# ---------------------------------------------------------
# FINAL CUSTOMER INSIGHT
# ---------------------------------------------------------

st.divider()

st.header("💼 Customer-Level Business Insight")

if customer["TARGET"] == 1:

    st.warning(
        """
        ⚠️ This customer has a historical payment-difficulty record.

        Review income, credit exposure, annuity burden and external
        indicators together for deeper financial assessment.
        """
    )

else:

    st.success(
        """
        ✅ This customer does not have a historical payment-difficulty
        record in the dataset.

        The profile can still be evaluated using income, credit exposure,
        repayment obligation and external indicators.
        """
    )