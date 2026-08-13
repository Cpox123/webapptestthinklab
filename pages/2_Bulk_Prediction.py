import pandas as pd
import streamlit as st

from config.project_data import (
    BULK_ROW_LIMIT,
    LABEL_ORDER,
    REVIEW_COLUMN_CANDIDATES,
)
from services import ui_service as ui
from services.bulk_service import predict_bulk

ui.apply_theme()
ui.render_brand()

ui.render_page_header(
    "Bulk CSV Prediction",
    "Upload a CSV file containing reviews and get predictions for all "
    "of them at once.",
)

REVIEW_COLUMN = "Review Text"
STATE_KEY = "bulk_results"
COUNTS_KEY = "bulk_counts"
UPLOAD_KEY = "bulk_uploader"


# --------------------------------------------------
# Upload zone (left) + requirements (right)
# --------------------------------------------------

upload_col, info_col = st.columns([1.45, 1.0], gap="large")

with upload_col:

    st.markdown(
        f'<div style="font-size:1.05rem; font-weight:700; '
        f'color:{ui.TEXT_DARK}; margin-bottom:6px;">📤 Upload CSV File</div>',
        unsafe_allow_html=True,
    )

    # Real text (not only inside the drop box) so the instructions are
    # always visible on every screen size.
    st.markdown(
        f'<div style="color:{ui.TEXT_MUTED}; font-size:0.9rem; '
        f'margin-bottom:10px;">Drag &amp; drop your CSV file into the box '
        f'below, or click <b>Browse files</b>. Supports <b>.csv</b> files '
        f'up to 200MB.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            label_visibility="collapsed",
            key=UPLOAD_KEY,
        )

    st.info(
        "ℹ️ After uploading, you will be able to preview the data, "
        "run predictions, and download the results."
    )

with info_col:

    st.markdown(
        ui.bulk_requirements_html(BULK_ROW_LIMIT, REVIEW_COLUMN_CANDIDATES),
        unsafe_allow_html=True,
    )

    st.markdown(
        ui.example_csv_html(),
        unsafe_allow_html=True,
    )

st.divider()

if uploaded_file is None:
    # Reset state once nothing is uploaded
    st.session_state.pop(STATE_KEY, None)
    st.stop()


# --------------------------------------------------
# Read the CSV robustly
# --------------------------------------------------

def read_csv_safely(file):
    """Read an uploaded CSV, falling back to latin-1 for legacy encodings."""

    try:
        return pd.read_csv(file, encoding="utf-8")

    except UnicodeDecodeError:
        file.seek(0)
        return pd.read_csv(file, encoding="latin-1")

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
        st.stop()

    except pd.errors.ParserError:
        st.error("The uploaded file is not a valid CSV.")
        st.stop()


def find_review_column(df):
    """Locate the review text column using the accepted names."""

    lookup = {str(column).strip().lower(): column for column in df.columns}

    for candidate in REVIEW_COLUMN_CANDIDATES:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]

    return None


df = read_csv_safely(uploaded_file)

if df.empty:
    st.error("The uploaded CSV contains no data rows.")
    st.stop()

# A new file invalidates previous results
file_identity = f"{uploaded_file.name}-{len(df)}"

previous = st.session_state.get(STATE_KEY)

if previous is not None and previous["file_identity"] != file_identity:
    st.session_state.pop(STATE_KEY)
    previous = None


# --------------------------------------------------
# Preview and validation
# --------------------------------------------------

st.subheader("CSV Preview")
st.dataframe(df.head(), width="stretch", hide_index=True)

review_column = find_review_column(df)

if review_column is None:

    st.error(
        "No review text column found. Your CSV must contain one of: "
        + ", ".join(f"**{name}**" for name in REVIEW_COLUMN_CANDIDATES)
        + f". Found columns: {', '.join(df.columns)}"
    )
    st.stop()

if review_column != REVIEW_COLUMN:

    df = df.rename(columns={review_column: REVIEW_COLUMN})
    st.caption(f"Using column **'{review_column}'** as the review text.")

# Enforce the bulk row limit
if len(df) > BULK_ROW_LIMIT:

    st.warning(
        f"The file contains {len(df)} reviews, which is more than the "
        f"{BULK_ROW_LIMIT}-review bulk limit. Only the first "
        f"{BULK_ROW_LIMIT} reviews will be classified."
    )
    df = df.head(BULK_ROW_LIMIT)

# Clean the review column
df[REVIEW_COLUMN] = df[REVIEW_COLUMN].fillna("").astype(str).str.strip()

empty_count = int((df[REVIEW_COLUMN] == "").sum())
valid_count = len(df) - empty_count

st.subheader("Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(df))
col2.metric("Valid Reviews", valid_count)
col3.metric("Empty Reviews", empty_count)

if empty_count > 0:
    st.warning(
        f"{empty_count} empty review(s) found. "
        "They will be marked as 'Invalid review'."
    )


# --------------------------------------------------
# Run prediction
# --------------------------------------------------

predict_clicked = st.button(
    "🚀 Predict All",
    type="primary",
    disabled=(valid_count == 0),
)

if valid_count == 0:
    st.error("There are no valid reviews to predict.")

if predict_clicked:

    progress_bar = st.progress(
        0.0,
        text="Classifying reviews...",
    )

    def update_progress(done, total):
        progress_bar.progress(
            done / total,
            text=f"Classifying reviews... {done}/{total}",
        )

    predictions = predict_bulk(
        df[REVIEW_COLUMN].tolist(),
        progress_callback=update_progress,
    )

    progress_bar.empty()

    result_df = df.copy()

    result_df["Predicted Sentiment"] = [
        item["prediction"] for item in predictions
    ]

    result_df["Confidence"] = [
        round(item["confidence"], 4)
        if item["confidence"] is not None
        else None
        for item in predictions
    ]

    counts = (
        result_df["Predicted Sentiment"]
        .value_counts()
        .reindex(LABEL_ORDER, fill_value=0)
    )

    st.session_state[STATE_KEY] = {
        "file_identity": file_identity,
        "result_df": result_df,
    }

    # Shared with the Dashboard page
    st.session_state[COUNTS_KEY] = {
        "Negative": int(counts["Negative"]),
        "Neutral": int(counts["Neutral"]),
        "Positive": int(counts["Positive"]),
        "Total": int(counts.sum()),
    }


# --------------------------------------------------
# Results (persist across reruns so the download works)
# --------------------------------------------------

state = st.session_state.get(STATE_KEY)

if (
    state is not None
    and state["file_identity"] == file_identity
):

    result_df = state["result_df"]

    st.subheader("Prediction Results")

    st.dataframe(
        ui.style_results_table(result_df),
        width="stretch",
        hide_index=True,
        column_config={
            "Confidence": st.column_config.ProgressColumn(
                "Confidence",
                format="%.2f",
                min_value=0.0,
                max_value=1.0,
            ),
        },
    )

    # Distribution of valid predictions
    counts = (
        result_df["Predicted Sentiment"]
        .value_counts()
        .reindex(LABEL_ORDER, fill_value=0)
    )

    total_valid = int(counts.sum())

    st.subheader("Sentiment Distribution")

    chart_left, chart_right = st.columns([1.0, 1.0], gap="large")

    with chart_left:

        donut_parts = [
            (
                label,
                100.0 * int(counts[label]) / total_valid
                if total_valid
                else 0.0,
            )
            for label in ["Positive", "Neutral", "Negative"]
        ]

        st.markdown(
            ui.panel_html(
                ui.donut_chart_html(
                    donut_parts,
                    center_value=f"{total_valid:,}",
                    center_label="Total",
                ),
                "Sentiment Share",
                "🥧",
            ),
            unsafe_allow_html=True,
        )

    with chart_right:

        st.markdown(
            ui.panel_html(
                ui.vbar_chart_html(counts.to_dict()),
                "Sentiment Counts",
                "📊",
            ),
            unsafe_allow_html=True,
        )

    # Download persists in session state, so it survives reruns.
    # on_click="ignore" avoids a full page reload on download click.
    csv_data = result_df.to_csv(index=False)

    action_left, action_right = st.columns([1.0, 1.0])

    with action_left:
        st.download_button(
            "⬇️ Download Results CSV",
            data=csv_data.encode("utf-8-sig"),
            file_name="sentiment_predictions.csv",
            mime="text/csv",
            type="primary",
            key="bulk_download",
            on_click="ignore",
            width="stretch",
        )

    with action_right:
        clear_clicked = st.button(
            "🧹 Clear Results",
            width="stretch",
        )

    if clear_clicked:
        st.session_state.pop(STATE_KEY, None)
        st.session_state.pop(COUNTS_KEY, None)
        st.session_state.pop(UPLOAD_KEY, None)
        st.rerun()

    st.caption(
        "If the download does not start (some embedded app previews block "
        "downloads), open the app in a normal browser tab - or copy the CSV "
        "from below."
    )

    # Fallback that works even where file downloads are blocked
    with st.expander("Copy the CSV manually"):
        st.write(
            "Click the copy icon in the top-right corner of the box, then "
            "paste into a file named sentiment_predictions.csv"
        )
        st.code(csv_data, language="csv")

ui.render_footer()
