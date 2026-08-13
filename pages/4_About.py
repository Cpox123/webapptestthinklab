import streamlit as st

from config.project_data import (
    COURSE,
    DATASET_NAME,
    DATASET_REVIEW_COUNT,
    DATASET_SOURCE,
    FINAL_MODEL_NAME,
    GROUP_NAME,
    MODEL_TYPES,
    MODEL_RESULTS,
    PIPELINE_STEPS,
    TEAM_MEMBERS,
)
from services import ui_service as ui

ui.apply_theme()
ui.render_brand()

ui.render_page_header(
    "About This Project",
    f"This project was developed as part of the {COURSE} module. "
    "It follows the complete NLP pipeline and compares multiple models.",
)

# --------------------------------------------------
# NLP pipeline
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        ui.pipeline_html(PIPELINE_STEPS),
        "NLP Pipeline",
        "🔀",
    ),
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Dataset + Models
# --------------------------------------------------

left, right = st.columns([1.0, 1.0], gap="large")

with left:

    st.markdown(
        ui.panel_html(
            '<div style="display:flex; align-items:center; gap:14px; '
            'margin-bottom:10px;">'
            f'<div style="width:48px; height:48px; border-radius:12px; '
            f'background:{ui.METRIC_COLORS["blue"]}1A; '
            f'color:{ui.METRIC_COLORS["blue"]}; font-size:1.4rem; '
            'display:flex; align-items:center; justify-content:center;">🗄️'
            "</div>"
            "<div>"
            f'<div style="font-weight:700; color:{ui.TEXT_DARK};">'
            f"{DATASET_NAME}</div>"
            f'<div style="font-size:0.82rem; color:{ui.TEXT_MUTED};">'
            f"{DATASET_REVIEW_COUNT} reviews</div>"
            "</div></div>"
            f'<div style="display:flex; justify-content:space-between; '
            f'border-top:1px dashed #E6ECF7; padding-top:10px;">'
            f'<span style="color:{ui.TEXT_MUTED}; font-size:0.85rem;">Source</span>'
            f'<span style="color:{ui.ACCENT}; font-size:0.85rem; '
            f'font-weight:600;">{DATASET_SOURCE}</span>'
            "</div>"
            f'<div style="color:{ui.TEXT_MUTED}; font-size:0.85rem; '
            f'margin-top:10px; line-height:1.6;">Customer reviews of clothing '
            "products, with ratings used to derive sentiment labels "
            "(Positive = 4–5 ★, Neutral = 3 ★, Negative = 1–2 ★)."
            "</div>",
            "Dataset",
            "📚",
        ),
        unsafe_allow_html=True,
    )

with right:

    model_rows = "".join(
        ui.model_badge_html(
            name,
            MODEL_TYPES.get(name, "ML"),
            name == FINAL_MODEL_NAME,
        )
        for name in MODEL_RESULTS
    )

    st.markdown(
        ui.panel_html(model_rows, "Models Implemented", "🏆"),
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Team
# --------------------------------------------------

st.markdown(
    f'<div style="font-size:1.05rem; font-weight:700; color:{ui.TEXT_DARK}; '
    f'margin:14px 0 10px 0;">👥 Team Members ({GROUP_NAME})</div>',
    unsafe_allow_html=True,
)

team_cols = st.columns(len(TEAM_MEMBERS))
for col, member in zip(team_cols, TEAM_MEMBERS):
    with col:
        st.markdown(ui.team_card_html(member), unsafe_allow_html=True)

st.caption("Edit team details in config/project_data.py")

# --------------------------------------------------
# Ethics & limitations
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        f'<div style="color:{ui.TEXT_MUTED}; font-size:0.9rem; '
        f'line-height:1.7;">'
        "The dataset contains customer reviews and may contain class imbalance. "
        "This can affect the model's ability to identify minority sentiment "
        "classes, especially Neutral reviews. "
        "Model predictions should be treated as automated classifications and "
        "should not be considered perfect representations of customer opinions. "
        "The system is trained on a specific product review dataset, so "
        "performance may differ when it is used on reviews from other products, "
        "platforms, or writing styles."
        "</div>",
        "Ethics, Bias & Limitations",
        "⚖️",
    ),
    unsafe_allow_html=True,
)

ui.render_footer()
