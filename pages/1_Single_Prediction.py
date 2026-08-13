import streamlit as st

from services.prediction_service import predict_sentiment
from services import ui_service as ui


# Apply shared app styling
ui.apply_theme()
ui.render_brand()


# Page header
ui.render_page_header(
    "Single Review Prediction",
    "Enter a customer review and predict its sentiment.",
)


# Review input
review = st.text_area(
    "Product Review",
    placeholder="Example: The dress is beautiful and comfortable.",
    height=150,
)


# Prediction button
if st.button(
    "Predict Sentiment",
    type="primary",
):

    if not review.strip():

        st.warning(
            "Please enter a review."
        )

    else:

        result = predict_sentiment(review)

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


# Footer
ui.render_footer()
