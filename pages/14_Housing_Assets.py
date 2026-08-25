import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Housing & Assets", page_icon="🏠", layout="wide")

df = preprocess_data(load_data())

st.title("🏠 Housing & Asset Analysis")
st.caption("Housing situation, vehicle and property ownership")
st.divider()

st.header("🏠 Housing Type")

housing = df["NAME_HOUSING_TYPE"].value_counts().reset_index()
housing.columns = ["Housing Type", "Customers"]

fig = px.treemap(
    housing,
    path=["Housing Type"],
    values="Customers",
    color="Customers",
    color_continuous_scale="Purples"
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Housing distribution provides a quick overview of
    the living situations represented in the portfolio.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚗 Car Ownership")

    car = df["FLAG_OWN_CAR"].value_counts().reset_index()
    car.columns = ["Ownership", "Customers"]

    fig = px.pie(
        car,
        names="Ownership",
        values="Customers",
        hole=.58,
        color_discrete_sequence=[
            "#7E57C2",
            "#D1A3FF"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("🏡 Property Ownership")

    property_data = df["FLAG_OWN_REALTY"].value_counts().reset_index()
    property_data.columns = ["Ownership", "Customers"]

    fig = px.pie(
        property_data,
        names="Ownership",
        values="Customers",
        hole=.58,
        color_discrete_sequence=[
            "#7E57C2",
            "#D1A3FF"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    🧠 **Insight:** Vehicle and property ownership provide additional
    information about the customer's financial profile.
    """
)

st.header("🎯 Housing Type vs Default Rate")

risk = (
    df.groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values()
    .reset_index()
)

risk.columns = ["Housing Type", "Default Rate"]

fig = px.bar(
    risk,
    x="Default Rate",
    y="Housing Type",
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
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.success(
    """
    💼 **Business Insight:** Housing and asset ownership can supplement
    financial analysis but should not independently determine credit decisions.
    """
)