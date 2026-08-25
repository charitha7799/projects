import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Home Credit Default Risk",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM DASHBOARD DESIGN
# ==========================================

st.markdown(
    """
    <style>

    /* Main Background */

    .stApp {

        background:
        radial-gradient(
            circle at 10% 5%,
            rgba(37, 99, 235, 0.18),
            transparent 25%
        ),

        radial-gradient(
            circle at 90% 10%,
            rgba(124, 58, 237, 0.16),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #07111f,
            #0d1728 48%,
            #111827
        );

    }


    /* Sidebar */

    [data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #06101d,
            #101a2d
        );

        border-right:
        1px solid
        rgba(148, 163, 184, 0.15);

    }


    /* Main Container */

    .block-container {

        padding-top: 2rem;

        max-width: 1500px;

    }


    /* KPI Cards */

    div[data-testid="stMetric"] {

        background:
        rgba(15, 23, 42, 0.80);

        border:
        1px solid
        rgba(148, 163, 184, 0.16);

        border-radius: 16px;

        padding: 15px;

        box-shadow:
        0 8px 28px
        rgba(0, 0, 0, 0.20);

    }


    div[data-testid="stMetricLabel"] {

        color:
        #94a3b8 !important;

    }


    div[data-testid="stMetricValue"] {

        color:
        #f8fafc !important;

    }


    /* Insight Cards */

    .insight {

        background:
        rgba(15, 23, 42, 0.80);

        border:
        1px solid
        rgba(148, 163, 184, 0.14);

        border-radius: 15px;

        padding:
        15px 18px;

        margin:
        8px 0;

    }


    .risk {

        border-left:
        5px solid #ef4444;

    }


    .watch {

        border-left:
        5px solid #f59e0b;

    }


    .good {

        border-left:
        5px solid #22c55e;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏦 Home Credit")

st.sidebar.caption(
    "Default Risk Intelligence Dashboard"
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    This dashboard analyzes:

    • Customer profile

    • Loan applications

    • Default risk

    • Income & credit

    • Repayment burden

    • External credit signals

    • Business insights
    """
)


# ==========================================
# HOME PAGE
# ==========================================

st.title("🏦 Home Credit Default Risk Analytics")

st.subheader(
    "Business Intelligence Dashboard for Credit Risk Analysis"
)

st.markdown(
    """
    ### Welcome 👋

    This dashboard analyzes customer applications and identifies
    patterns associated with repayment difficulties.

    **Business objective:**

    Help financial institutions understand customer risk,
    affordability and portfolio-level default patterns.
    """
)

st.markdown("---")

st.info(
    "👈 Use the pages in the sidebar to explore the complete analysis."
)