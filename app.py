
import streamlit as st

from config.project_data import (
    DATASET_NAME,
    DATASET_REVIEW_COUNT,
    DATASET_SENTIMENT_SPLIT,
    FINAL_MODEL_NAME,
    MODEL_INFO,
    MODEL_RESULTS,
)
from services import ui_service as ui

st.set_page_config(
    page_title="ThinkLab Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    # Sidebar starts hidden; it opens by clicking the top-left brand bar
    initial_sidebar_state="collapsed",
)

ui.apply_theme()
ui.render_brand()

# --------------------------------------------------
# Home page content
# --------------------------------------------------

def home_page():

    # Top-right group chip
    from config.project_data import GROUP_NAME

    st.markdown(
        '<div style="display:flex; justify-content:flex-end;">'
        f'<span style="background:{ui.NAVY}; color:#FFFFFF; font-weight:600; '
        'font-size:0.85rem; padding:7px 14px; border-radius:999px; '
        'box-shadow:0 4px 10px rgba(13,27,62,0.25);">'
        f"🧠 {GROUP_NAME}</span></div>",
        unsafe_allow_html=True,
    )

    hero_left, hero_right = st.columns([1.45, 1.0], gap="large")

    with hero_left:

        st.markdown(
            f'<div style="font-size:2.3rem; font-weight:800; color:{ui.ACCENT}; '
            f'margin-bottom:6px; line-height:1.2; margin-top:0.4rem;">'
            "Welcome to NLP Sentiment Analyzer</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div style="color:{ui.TEXT_MUTED}; font-size:1.02rem; '
            f'max-width:520px;">'
            "An end-to-end Natural Language Processing application for product "
            "review sentiment analysis using BERT — our final and "
            "best-performing model. It classifies reviews into "
            "<b style='color:#30A46C;'>Positive</b> 🟢, "
            "<b style='color:#F5A524;'>Neutral</b> 🟡 and "
            "<b style='color:#E5484D;'>Negative</b> 🔴 sentiments."
            "</div>",
            unsafe_allow_html=True,
        )

    with hero_right:

        st.image("assets/robot_hero.png")

    st.write("")

    final_accuracy = MODEL_RESULTS[FINAL_MODEL_NAME]["accuracy"]
    final_f1 = MODEL_RESULTS[FINAL_MODEL_NAME]["macro_f1"]

    ui.render_stat_cards(
        [
            ("🗄️", "Dataset", f"{DATASET_NAME}",
             f"{DATASET_REVIEW_COUNT} reviews", ui.METRIC_COLORS["blue"]),
            ("🤖", "Final Model", MODEL_INFO["Model"],
             "Transformer Model", ui.METRIC_COLORS["green"]),
            ("🎯", "Accuracy", f"{final_accuracy * 100:.2f}%",
             "Test set accuracy", ui.METRIC_COLORS["purple"]),
            ("⭐", "Macro F1 Score", f"{final_f1:.2f}",
             "Best among all models", ui.METRIC_COLORS["orange"]),
        ]
    )

    st.write("")

    dist_col, about_col = st.columns([1.0, 1.0], gap="large")

    with dist_col:

        split_body = ui.donut_chart_html(
            [(label, pct) for label, pct in DATASET_SENTIMENT_SPLIT.items()],
            center_value=DATASET_REVIEW_COUNT,
            center_label="Reviews",
        )

        st.markdown(
            ui.panel_html(split_body, "Sentiment Distribution (Overall)", "📊"),
            unsafe_allow_html=True,
        )

        st.caption(
            "Labels derived from star ratings: Positive = 4–5 ★, "
            "Neutral = 3 ★, Negative = 1–2 ★ (approximate)."
        )

    with about_col:

        st.markdown(
            ui.panel_html(
                f'<div style="color:{ui.TEXT_MUTED}; font-size:0.95rem; '
                f'line-height:1.7;">This application classifies product '
                f"reviews into Positive, Neutral, or Negative sentiments. Six "
                f"models were implemented and compared — and <b>BERT</b> "
                f"achieved the best performance, so it powers this final "
                f"application.</div>",
                "About the Project",
                "ℹ️",
            ),
            unsafe_allow_html=True,
        )

        st.write("")
        st.page_link(
            "pages/1_Single_Prediction.py",
            label="Explore the Application →",
            icon="🚀",
        )

    ui.render_footer()


# --------------------------------------------------
# Navigation
# --------------------------------------------------

pg = st.navigation(
    [
        st.Page(home_page, title="Home", icon=":material/home:", default=True),
        st.Page("pages/1_Single_Prediction.py",
                title="Single Prediction", icon=":material/edit:"),
        st.Page("pages/2_Bulk_Prediction.py",
                title="Bulk Prediction", icon=":material/folder_open:"),
        st.Page("pages/3_Dashboard.py",
                title="Dashboard", icon=":material/bar_chart:"),
        st.Page("pages/4_About.py",
                title="About", icon=":material/info:"),
    ]
)

pg.run()
