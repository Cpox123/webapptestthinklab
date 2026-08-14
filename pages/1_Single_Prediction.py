import streamlit as st

from services.prediction_service import predict_sentiment
from services import ui_service as ui


# Apply shared app styling
ui.apply_theme()
ui.render_brand()


# Page header
ui.render_page_header(
    "Single Review Prediction",
    "Enter a product review to classify it as Positive, Neutral, or Negative.",
)


# Review input
review = st.text_area(
    "Product Review",
    placeholder="Example: The dress is beautiful and comfortable.",
    height=150,
)


# Prediction button
if st.button(
    "🔍Analyze Review",
    type="primary",
):

    if not review.strip():

        st.warning(
            "Please enter a review."
        )

    else:

        st.session_state["single_result"] = predict_sentiment(review)


# Prediction result
result = st.session_state.get("single_result")

if result:

    st.subheader(
        "Prediction Result"
    )

    if result == "Positive":

        st.success(
            "😊 Positive"
        )

    elif result == "Negative":

        st.error(
            "😞 Negative"
        )

    elif result == "Neutral":

        st.info(
            "😐 Neutral"
        )

    else:

        st.warning(result)


    # Clear result
    if st.button(
        "🗑️ Clear Result"
    ):
        st.session_state.pop(
            "single_result",
            None,
        )
        st.rerun()


# Footer
ui.render_footer()
