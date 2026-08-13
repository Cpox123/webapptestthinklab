import streamlit as st
from services.prediction_service import predict_sentiment

st.title("Single Review Prediction")

st.write(
    "Enter a customer review and predict its sentiment."
)

review = st.text_area(
    "Product Review",
    placeholder="Example: The dress is beautiful and comfortable.",
    height=150
)

if st.button("Predict Sentiment"):

    if not review.strip():
        st.warning("Please enter a review.")

    else:
        result = predict_sentiment(review)

        st.subheader("Prediction Result")

        if result == "Positive":
            st.success("Positive")

        elif result == "Negative":
            st.error("Negative")

        elif result == "Neutral":
            st.info("Neutral")

        else:
            st.warning(result)
