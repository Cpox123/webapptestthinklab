import streamlit as st

from config.project_data import (
    FINAL_MODEL_NAME,
    MODEL_RESULTS,
    MODEL_TYPES,
)
from services import ui_service as ui


ui.apply_theme()
ui.render_brand()


# --------------------------------------------------
# Header
# --------------------------------------------------

ui.render_page_header(
    "Analytics Dashboard",
    "Compare all evaluated models, understand the final model selection, "
    "and explore sentiment analytics from bulk predictions.",
)


# --------------------------------------------------
# Dashboard overview
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        f'<div style="font-size:0.92rem; line-height:1.7; '
        f'color:{ui.TEXT_MUTED};">'
        "This dashboard summarizes the evaluation of all "
        "<b>six Machine Learning and Deep Learning models</b>. "
        "Accuracy shows overall prediction correctness, while "
        "<b>Macro F1</b> gives equal importance to Positive, Neutral, "
        "and Negative sentiment classes."
        "</div>",
        "Dashboard Overview",
        "💡",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Find key models
# --------------------------------------------------

ml_models = {
    name: result
    for name, result in MODEL_RESULTS.items()
    if MODEL_TYPES[name] == "ML"
}

dl_models = {
    name: result
    for name, result in MODEL_RESULTS.items()
    if MODEL_TYPES[name] == "DL"
}

highest_accuracy = max(
    MODEL_RESULTS,
    key=lambda name: MODEL_RESULTS[name]["accuracy"],
)

best_ml = max(
    ml_models,
    key=lambda name: ml_models[name]["macro_f1"],
)

best_dl = max(
    dl_models,
    key=lambda name: dl_models[name]["macro_f1"],
)

final = MODEL_RESULTS[FINAL_MODEL_NAME]


# --------------------------------------------------
# Key highlights
# --------------------------------------------------

st.subheader("Key Model Highlights")

ui.render_stat_cards(
    [
        (
            "🏆",
            "Highest Accuracy",
            highest_accuracy,
            f"{MODEL_RESULTS[highest_accuracy]['accuracy'] * 100:.2f}% accuracy",
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
            "Best DL & Final Model",
            best_dl,
            f"Macro F1: {dl_models[best_dl]['macro_f1']:.4f}",
            ui.METRIC_COLORS["green"],
        ),
    ]
)

st.write("")


# --------------------------------------------------
# Model comparison
# --------------------------------------------------

st.subheader("Model Performance Comparison")

st.caption(
    "Blue bars represent Accuracy and cyan bars represent Macro F1. "
    "The ⭐ indicates the final selected model."
)

# Better visual ordering: ML models first, then DL models
comparison_order = [
    "Logistic Regression",
    "Naive Bayes",
    "SVM",
    "LSTM",
    "CNN",
    "BERT",
]

comparison_results = {
    model: MODEL_RESULTS[model]
    for model in comparison_order
    if model in MODEL_RESULTS
}

st.markdown(
    ui.panel_html(
        ui.model_comparison_html(
            comparison_results,
            FINAL_MODEL_NAME,
        ),
        "All Six Evaluated Models",
        "📈",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Final model explanation
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        f'<div style="display:flex; align-items:flex-start; gap:14px;">'

        f'<div style="font-size:2rem;">⭐</div>'

        f'<div>'

        f'<div style="font-weight:800; font-size:1rem; '
        f'margin-bottom:6px;">'
        f"Why {FINAL_MODEL_NAME} Was Selected"
        f"</div>"

        f'<div style="font-size:0.88rem; line-height:1.7; '
        f'color:{ui.TEXT_MUTED};">'

        f"<b>{highest_accuracy}</b> achieved the highest overall "
        f"accuracy at "
        f"<b>{MODEL_RESULTS[highest_accuracy]['accuracy'] * 100:.2f}%</b>. "

        f"However, <b>{FINAL_MODEL_NAME}</b> achieved the highest "
        f"Macro F1 score of "
        f"<b>{final['macro_f1']:.4f}</b> with an accuracy of "
        f"<b>{final['accuracy'] * 100:.2f}%</b>. "

        f"Because the dataset is strongly imbalanced, Macro F1 was "
        f"considered more important for balanced performance across "
        f"all three sentiment classes. Therefore, "
        f"<b>{FINAL_MODEL_NAME}</b> was selected as the final model."

        f"</div>"
        f"</div>"
        f"</div>",
        "Final Model Selection",
        "🏆",
    ),
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Exact metrics
# --------------------------------------------------

with st.expander("📋 View Exact Model Metrics"):

    metrics_table = []

    for model in comparison_order:

        if model not in MODEL_RESULTS:
            continue

        result = MODEL_RESULTS[model]

        metrics_table.append(
            {
                "Model": model,
                "Type": MODEL_TYPES[model],
                "Accuracy": f"{result['accuracy'] * 100:.2f}%",
                "Macro F1": f"{result['macro_f1']:.4f}",
                "Final Model": "Yes" if model == FINAL_MODEL_NAME else "",
            }
        )

    st.dataframe(
        metrics_table,
        width="stretch",
        hide_index=True,
    )
# --------------------------------------------------
# Detailed model evaluation
# --------------------------------------------------

with st.expander("🔎 Detailed Model Evaluation"):

    st.caption(
        "Confusion matrices show how the two strongest models classified "
        "Negative, Neutral, and Positive reviews on the test set."
    )

    bert_col, svm_col = st.columns(2, gap="large")

    with bert_col:

        st.markdown("#### 🤖 BERT — Final Model")

        st.image(
            "assets/evaluation/bert_confusion_matrix.png",
            use_container_width=True,
        )

        st.caption(
            "BERT was selected as the final model because it achieved "
            "the highest Macro F1 score of 0.6600."
        )

    with svm_col:

        st.markdown("#### 🏆 SVM — Highest Accuracy")

        st.image(
            "assets/evaluation/svm_confusion_matrix.png",
            use_container_width=True,
        )

        st.caption(
            "SVM achieved the highest overall accuracy at 82.06%, "
            "but its Macro F1 score was lower than BERT."
        )

    st.info(
        "📌 BERT provides the stronger balanced performance across the "
        "three sentiment classes, while SVM provides the highest overall "
        "accuracy."
    )

# --------------------------------------------------
# Live prediction analytics
# --------------------------------------------------

st.divider()

st.subheader("Live Prediction Analytics")

st.caption(
    "These statistics are generated from Bulk Prediction results "
    "during the current application session."
)

counts = st.session_state.get("bulk_counts")


if not counts:

    st.info(
        "💡 No bulk prediction results are available yet. "
        "Run a Bulk CSV Prediction to generate live sentiment analytics."
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
            (
                "Positive",
                100 * positive / total if total else 0,
            ),
            (
                "Neutral",
                100 * neutral / total if total else 0,
            ),
            (
                "Negative",
                100 * negative / total if total else 0,
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
    # Quick session insight
    # --------------------------------------------------

    sentiment_counts = {
        "Positive": positive,
        "Neutral": neutral,
        "Negative": negative,
    }

    dominant_sentiment = max(
        sentiment_counts,
        key=sentiment_counts.get,
    )

    dominant_share = (
        100 * sentiment_counts[dominant_sentiment] / total
        if total
        else 0
    )

    st.info(
        f"📌 **Session Insight:** "
        f"**{dominant_sentiment}** is the most common predicted "
        f"sentiment, representing **{dominant_share:.2f}%** "
        f"of the {total:,} analyzed reviews."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

ui.render_footer()
