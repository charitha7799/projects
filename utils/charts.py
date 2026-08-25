import streamlit as st


def apply_dashboard_style():

    st.markdown("""
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background:
            radial-gradient(circle at top left, #173b63 0%, transparent 35%),
            radial-gradient(circle at bottom right, #123b48 0%, transparent 35%),
            linear-gradient(135deg, #071525, #0d2238, #102c40);
    }

    /* PAGE TITLE */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #dff8ff !important;
    }

    h3 {
        color: #9feaff !important;
    }

    /* KPI CARDS */
    .kpi {
        background: linear-gradient(
            145deg,
            rgba(38, 79, 111, 0.95),
            rgba(10, 29, 49, 0.95)
        );

        border: 1px solid rgba(120, 220, 255, 0.25);

        border-radius: 20px;

        padding: 22px;

        text-align: center;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.45),
            inset 0 1px 1px rgba(255,255,255,0.15);

        min-height: 125px;

        margin-bottom: 20px;
    }

    .kpi-title {
        color: #9eb9cc;
        font-size: 14px;
        font-weight: 500;
    }

    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-sub {
        color: #52d9ff;
        font-size: 12px;
        margin-top: 5px;
    }


    /* INSIGHT CARD */
    .insight {
        background: linear-gradient(
            135deg,
            rgba(20, 69, 95, 0.95),
            rgba(10, 35, 55, 0.95)
        );

        border-left: 5px solid #29d8ff;

        border-radius: 15px;

        padding: 20px;

        margin: 18px 0;

        color: #eafaff;

        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }

    .insight-title {
        color: #55ddff;
        font-size: 19px;
        font-weight: 800;
    }

    .insight-text {
        color: #e5f5fa;
        font-size: 15px;
        line-height: 1.7;
    }


    /* BUSINESS CARD */
    .business {
        background: linear-gradient(
            135deg,
            rgba(20, 75, 61, 0.95),
            rgba(9, 43, 37, 0.95)
        );

        border-left: 5px solid #39e39b;

        border-radius: 15px;

        padding: 20px;

        margin: 18px 0;

        color: #eafff5;

        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }

    .business-title {
        color: #4ff0aa;
        font-size: 19px;
        font-weight: 800;
    }

    .business-text {
        color: #e7fff5;
        font-size: 15px;
        line-height: 1.7;
    }


    /* STREAMLIT METRICS */
    [data-testid="stMetric"] {
        background: rgba(20, 50, 75, 0.8);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #071827,
            #0c2539
        );
    }

    /* BUTTON */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid #35d8ff;
        background: #123b54;
        color: white;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #1a5878;
    }

    </style>
    """, unsafe_allow_html=True)


def kpi_card(title, value, subtitle=""):

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight_box(title, text):

    st.markdown(
        f"""
        <div class="insight">

            <div class="insight-title">
                🧠 {title}
            </div>

            <div class="insight-text">
                {text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def business_box(title, text):

    st.markdown(
        f"""
        <div class="business">

            <div class="business-title">
                💼 {title}
            </div>

            <div class="business-text">
                {text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(7,25,42,0.65)",

        font=dict(
            color="white",
            size=13
        ),

        title_font=dict(
            color="#ffffff",
            size=20
        ),

        margin=dict(
            l=30,
            r=30,
            t=65,
            b=30
        ),

        hoverlabel=dict(
            bgcolor="#163d58",
            font_color="white"
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig