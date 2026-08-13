import streamlit as st

from config.project_data import (
    FINAL_MODEL_NAME,
    MODEL_INFO,
    MODEL_RESULTS,
)
from services import ui_service as ui

ui.apply_theme()
ui.render_brand()

ui.render_page_header(
    "Analytics Dashboard",
    "Performance comparison of all evaluated models, plus live "
    "prediction analytics from this session.",
)

# --------------------------------------------------
# Model performance comparison
# --------------------------------------------------

st.markdown(
    ui.panel_html(
        ui.model_comparison_html(MODEL_RESULTS, FINAL_MODEL_NAME),
        "Model Performance Comparison",
        "📈",
    ),
    unsafe_allow_html=True,
)

final = MODEL_RESULTS[FINAL_MODEL_NAME]

st.markdown(
    ui.panel_html(
        f'<div style="display:flex; align-items:center; gap:16px;">'
        f'<div style="font-size:2rem;">🏆</div>'
        f"<div>"
        f'<div style="font-weight:800; color:{ui.TEXT_DARK}; font-size:1.05rem;">'
        f"Best Performing Model: {FINAL_MODEL_NAME} "
        f'<span style="color:{ui.TEXT_MUTED}; font-weight:500;">— '
        f"selected as the final model</span></div>"
        f'<div style="color:{ui.TEXT_MUTED}; font-size:0.88rem; margin-top:3px;">'
        f"Accuracy {final['accuracy'] * 100:.2f}% &middot; "
        f"Macro F1 {final['macro_f1']:.2f}. Macro F1 is used as the main "
        f"comparison metric because the sentiment classes are imbalanced."
        f"</div></div></div>",
        "Final Model Selection",
        "⭐",
    ),
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Live prediction analytics (filled after a bulk run)
# --------------------------------------------------

counts = st.session_state.get("bulk_counts")

if not counts:

    st.info(
        "💡 No bulk predictions yet. Run a **Bulk CSV Prediction** and the "
        "session analytics will appear here."
    )

else:

    total = counts["Total"]
    positive = counts["Positive"]
    neutral = counts["Neutral"]
    negative = counts["Negative"]

    def share(n):
        return f"({(100.0 * n / total) if total else 0.0:.2f}%)"

    ui.render_stat_cards(
        [
            ("🗂️", "Total Reviews", f"{total:,}",
             "classified in this session", ui.METRIC_COLORS["blue"]),
            ("🟢", "Positive", f"{positive:,}",
             share(positive), ui.METRIC_COLORS["green"]),
            ("🟡", "Neutral", f"{neutral:,}",
             share(neutral), ui.METRIC_COLORS["yellow"]),
            ("🔴", "Negative", f"{negative:,}",
             share(negative), ui.METRIC_COLORS["red"]),
        ]
    )

    st.write("")

    donut_col, bar_col = st.columns([1.0, 1.0], gap="large")

    with donut_col:

        parts = [
            ("Positive", 100.0 * positive / total if total else 0.0),
            ("Neutral", 100.0 * neutral / total if total else 0.0),
            ("Negative", 100.0 * negative / total if total else 0.0),
        ]

        st.markdown(
            ui.panel_html(
                ui.donut_chart_html(parts, f"{total:,}", "Total"),
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
                "Sentiment Distribution (Bar)",
                "📊",
            ),
            unsafe_allow_html=True,
        )

ui.render_footer()
