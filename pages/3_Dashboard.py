import streamlit as st

from config.project_data import (
    FINAL_MODEL_NAME,
    MODEL_RESULTS,
    MODEL_TYPES,
)
from services import ui_service as ui


ui.apply_theme()
ui.render_brand()

ui.render_page_header(
    "Analytics Dashboard",
    "Compare all evaluated models and explore sentiment analytics "
    "from bulk predictions.",
)


# --------------------------------------------------
# Dashboard overview
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        "This dashboard compares all six Machine Learning and Deep "
        "Learning models using Accuracy and Macro F1. It also shows "
        "sentiment statistics generated from Bulk Prediction results.",
        "Dashboard Overview",
        "💡",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Model highlights
# --------------------------------------------------

ml_models = {
    name: result
    for name, result in MODEL_RESULTS.items()
    if MODEL_TYPES[name] == "ML"
}

highest_accuracy = max(
    MODEL_RESULTS,
    key=lambda name: MODEL_RESULTS[name]["accuracy"],
)

best_ml = max(
    ml_models,
    key=lambda name: ml_models[name]["macro_f1"],
)

final = MODEL_RESULTS[FINAL_MODEL_NAME]


ui.render_stat_cards(
    [
        (
            "🏆",
            "Highest Accuracy",
            highest_accuracy,
            f"{MODEL_RESULTS[highest_accuracy]['accuracy'] * 100:.2f}%",
            ui.METRIC_COLORS["blue"],
        ),
        (
            "📊",
            "Best ML Macro F1",
            best_ml,
            f"Macro F1: {ml_models[best_ml]['macro_f1']:.4f}",
            ui.METRIC_COLORS["purple"],
        ),
        (
            "🤖",
            "Best DL / Final Model",
            FINAL_MODEL_NAME,
            f"Macro F1: {final['macro_f1']:.4f}",
            ui.METRIC_COLORS["green"],
        ),
    ]
)

st.write("")


# --------------------------------------------------
# Model performance comparison
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        ui.model_comparison_html(
            MODEL_RESULTS,
            FINAL_MODEL_NAME,
        ),
        "Model Performance Comparison",
        "📈",
    ),
    unsafe_allow_html=True,
)


st.info(
    f"📌 **{highest_accuracy}** achieved the highest accuracy at "
    f"**{MODEL_RESULTS[highest_accuracy]['accuracy'] * 100:.2f}%**, "
    f"while **{FINAL_MODEL_NAME}** achieved the highest Macro F1 "
    f"score of **{final['macro_f1']:.4f}**. Because the dataset is "
    f"imbalanced, BERT was selected as the final model."
)


# --------------------------------------------------
# Live prediction analytics
# --------------------------------------------------

st.subheader("Live Prediction Analytics")

counts = st.session_state.get("bulk_counts")


if not counts:

    st.info(
        "💡 No bulk predictions yet. Run a **Bulk CSV Prediction** "
        "to display session analytics here."
    )

else:

    total = counts["Total"]
    positive = counts["Positive"]
    neutral = counts["Neutral"]
    negative = counts["Negative"]

    def share(value):
        return f"{(100 * value / total) if total else 0:.2f}%"

    ui.render_stat_cards(
        [
            (
                "🗂️",
                "Total Reviews",
                f"{total:,}",
                "classified this session",
                ui.METRIC_COLORS["blue"],
            ),
            (
                "🟢",
                "Positive",
                f"{positive:,}",
                share(positive),
                ui.METRIC_COLORS["green"],
            ),
            (
                "🟡",
                "Neutral",
                f"{neutral:,}",
                share(neutral),
                ui.METRIC_COLORS["yellow"],
            ),
            (
                "🔴",
                "Negative",
                f"{negative:,}",
                share(negative),
                ui.METRIC_COLORS["red"],
            ),
        ]
    )

    st.write("")

    donut_col, bar_col = st.columns(
        [1.0, 1.0],
        gap="large",
    )

    with donut_col:

        parts = [
            ("Positive", 100 * positive / total if total else 0),
            ("Neutral", 100 * neutral / total if total else 0),
            ("Negative", 100 * negative / total if total else 0),
        ]

        st.markdown(
            ui.panel_html(
                ui.donut_chart_html(
                    parts,
                    f"{total:,}",
                    "Total",
                ),
                "Sentiment Distribution",
                "🥧",
            ),
            unsafe_allow_html=True,
        )

    with bar_col:

        st.markdown(
            ui.panel_html(
                ui.vbar_chart_html(
                    {
                        "Positive": positive,
                        "Neutral": neutral,
                        "Negative": negative,
                    }
                ),
                "Sentiment Counts",
                "📊",
            ),
            unsafe_allow_html=True,
        )


ui.render_footer()
