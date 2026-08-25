import streamlit as st

from utils.charts import apply_dashboard_style


def setup_page(title, subtitle):

    st.set_page_config(
        page_title=title,
        page_icon="🏦",
        layout="wide"
    )

    apply_dashboard_style()

    st.title("🏦 " + title)

    st.markdown(
        f"""
        <p style="
        color:#9ec8df;
        font-size:17px;
        margin-top:-15px;
        margin-bottom:25px;
        ">
        {subtitle}
        </p>
        """,
        unsafe_allow_html=True
    )


def section_title(title):

    st.markdown(
        f"""
        <h2 style="
        margin-top:25px;
        color:#bcefff;
        ">
        {title}
        </h2>
        """,
        unsafe_allow_html=True
    )


def divider():

    st.markdown(
        """
        <hr style="
        border:0;
        height:1px;
        background:linear-gradient(
            90deg,
            transparent,
            #35d5ff,
            transparent
        );
        ">
        """,
        unsafe_allow_html=True
    )