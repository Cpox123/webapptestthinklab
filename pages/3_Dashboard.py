import streamlit as st

from config.project_data import (
    FINAL_MODEL_NAME,
    MODEL_INFO,
    MODEL_RESULTS,
    MODEL_TYPES,
)
from services import ui_service as ui


ui.apply_theme()
ui.render_brand()


# --------------------------------------------------
# Page header
# --------------------------------------------------

ui.render_page_header(
    "Analytics Dashboard",
    "Compare all six Machine Learning and Deep Learning models, "
    "understand why BERT was selected, and explore sentiment "
    "analytics from bulk predictions.",
)


# --------------------------------------------------
# Dashboard introduction
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        f'<div style="color:{ui.TEXT_MUTED}; font-size:0.94rem; '
        f'line-height:1.7;">'
        "This dashboard provides an overview of the model evaluation "
        "results from the project. It compares the performance of all "
        "six implemented models using <b>Accuracy</b> and "
        "<b>Macro F1 Score</b>. It also displays live sentiment "
        "statistics when a Bulk CSV Prediction is completed during "
        "the current session."
        "</div>",
        "What This Dashboard Shows",
        "💡",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Calculate model highlights
# --------------------------------------------------

ml_results = {
    name: result
    for name, result in MODEL_RESULTS.items()
    if MODEL_TYPES.get(name) == "ML"
}

dl_results = {
    name: result
    for name, result in MODEL_RESULTS.items()
    if MODEL_TYPES.get(name) == "DL"
}


highest_accuracy_model = max(
    MODEL_RESULTS,
    key=lambda name: MODEL_RESULTS[name]["accuracy"],
)

best_ml_f1_model = max(
    ml_results,
    key=lambda name: ml_results[name]["macro_f1"],
)

best_dl_f1_model = max(
    dl_results,
    key=lambda name: dl_results[name]["macro_f1"],
)


highest_accuracy = MODEL_RESULTS[highest_accuracy_model]["accuracy"]
best_ml_f1 = ml_results[best_ml_f1_model]["macro_f1"]
best_dl_f1 = dl_results[best_dl_f1_model]["macro_f1"]


# --------------------------------------------------
# Key model highlights
# --------------------------------------------------

st.subheader("Key Model Highlights")

ui.render_stat_cards(
    [
        (
            "🏆",
            "Highest Accuracy",
            highest_accuracy_model,
            f"{highest_accuracy * 100:.2f}% accuracy",
            ui.METRIC_COLORS["blue"],
        ),
        (
            "📊",
            "Best ML Macro F1",
            best_ml_f1_model,
            f"Macro F1: {best_ml_f1:.4f}",
            ui.METRIC_COLORS["purple"],
        ),
        (
            "🤖",
            "Best DL / Final Model",
            best_dl_f1_model,
            f"Macro F1: {best_dl_f1:.4f}",
            ui.METRIC_COLORS["green"],
        ),
    ]
)

st.write("")

st.info(
    "📌 **Model selection summary:** "
    f"**{highest_accuracy_model}** achieved the highest overall "
    f"accuracy at **{highest_accuracy * 100:.2f}%**. "
    f"Among the Machine Learning models, **{best_ml_f1_model}** "
    f"achieved the highest Macro F1 score of **{best_ml_f1:.4f}**. "
    f"Among the Deep Learning models, **{best_dl_f1_model}** "
    f"achieved the highest Macro F1 score of **{best_dl_f1:.4f}**. "
    "Because the dataset is imbalanced, Macro F1 was given greater "
    "importance when selecting the final model."
)


# --------------------------------------------------
# Model performance comparison
# --------------------------------------------------

st.subheader("Model Performance Comparison")

st.caption(
    "Accuracy measures overall prediction correctness, while Macro F1 "
    "gives equal importance to the Positive, Neutral, and Negative "
    "sentiment classes."
)

st.markdown(
    ui.panel_html(
        ui.model_comparison_html(
            MODEL_RESULTS,
            FINAL_MODEL_NAME,
        ),
        "All Six Evaluated Models",
        "📈",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Final model selection
# --------------------------------------------------

final = MODEL_RESULTS[FINAL_MODEL_NAME]

st.markdown(
    ui.panel_html(
        f'<div style="display:flex; align-items:flex-start; gap:16px;">'

        f'<div style="font-size:2.2rem;">🏆</div>'

        f'<div style="flex:1;">'

        f'<div style="font-weight:800; '
        f'font-size:1.08rem; margin-bottom:7px;">'
        f"Final Selected Model: {FINAL_MODEL_NAME}"
        f"</div>"

        f'<div style="font-size:0.9rem; '
        f'line-height:1.65; opacity:0.75;">'

        f"<b>{FINAL_MODEL_NAME}</b> achieved an accuracy of "
        f"<b>{final['accuracy'] * 100:.2f}%</b> and the highest "
        f"overall Macro F1 score of "
        f"<b>{final['macro_f1']:.4f}</b>. "

        f"Although <b>{highest_accuracy_model}</b> achieved the "
        f"highest overall accuracy, its advantage in accuracy was "
        f"small compared with BERT. "

        f"Since the dataset contains a strong class imbalance, "
        f"Macro F1 provides a more balanced evaluation across "
        f"Positive, Neutral, and Negative classes. "

        f"For this reason, <b>{FINAL_MODEL_NAME}</b> was selected "
        f"as the final model and integrated into the application."

        f"</div>"

        f"</div>"
        f"</div>",
        "Why BERT Was Selected",
        "⭐",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Live prediction analytics
# --------------------------------------------------

st.subheader("Live Prediction Analytics")

st.caption(
    "This section is updated using predictions generated from the "
    "Bulk Prediction page during the current application session."
)

counts = st.session_state.get("bulk_counts")


if not counts:

    st.info(
        "💡 No bulk prediction results are available yet. "
        "Upload a CSV file and run **Bulk Prediction** to display "
        "live sentiment analytics here."
    )

    st.page_link(
        "pages/2_Bulk_Prediction.py",
        label="Go to Bulk Prediction →",
        icon="📂",
    )


else:

    total = counts["Total"]
    positive = counts["Positive"]
    neutral = counts["Neutral"]
    negative = counts["Negative"]


    def share(number):
        return (
            f"{(100.0 * number / total) if total else 0.0:.2f}%"
        )


    # --------------------------------------------------
    # Session statistics
    # --------------------------------------------------

    ui.render_stat_cards(
        [
            (
                "🗂️",
                "Total Reviews",
                f"{total:,}",
                "classified in this session",
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


    # --------------------------------------------------
    # Session sentiment charts
    # --------------------------------------------------

    donut_col, bar_col = st.columns(
        [1.0, 1.0],
        gap="large",
    )


    with donut_col:

        parts = [
            (
                "Positive",
                100.0 * positive / total
                if total
                else 0.0,
            ),
            (
                "Neutral",
                100.0 * neutral / total
                if total
                else 0.0,
            ),
            (
                "Negative",
                100.0 * negative / total
                if total
                else 0.0,
            ),
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


    # --------------------------------------------------
    # Session interpretation
    # --------------------------------------------------

    dominant_label = max(
        ["Positive", "Neutral", "Negative"],
        key=lambda label: counts[label],
    )

    dominant_count = counts[dominant_label]

    dominant_share = (
        100.0 * dominant_count / total
        if total
        else 0.0
    )

    st.info(
        f"📊 **Current session insight:** "
        f"The most common predicted sentiment is "
        f"**{dominant_label}**, representing "
        f"**{dominant_share:.2f}%** of the "
        f"{total:,} classified reviews."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

ui.render_footer()
