import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="External Score Analysis",
    page_icon="📊",
    layout="wide"
)

df = preprocess_data(load_data())

st.title("📊 External Score Analysis")
st.caption("External credit indicators and historical repayment outcomes")
st.divider()

scores = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

sample = df.sample(
    min(15000, len(df)),
    random_state=42
)

for score in scores:

    if score not in df.columns:
        continue

    st.header(f"🔎 {score}")

    fig = px.violin(
        sample,
        x="TARGET",
        y=score,
        color="TARGET",
        box=True,
        points=False,
        color_discrete_sequence=[
            "#B388FF",
            "#6A1B9A"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Historical Target",
        yaxis_title=score
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        f"""
        🧠 **Insight:** {score} allows comparison of external credit
        information between customers with different historical repayment
        outcomes.
        """
    )

st.header("🔥 External Score Correlation")

available = [
    x for x in scores
    if x in df.columns
]

corr = df[available + ["TARGET"]].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="Purples",
    aspect="auto"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success(
    """
    💼 **Business Insight:** External scores can provide powerful
    supporting signals when combined with income, credit exposure,
    repayment burden and customer characteristics.
    """
)