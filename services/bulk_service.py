from services.prediction_service import predict_batch_with_probabilities


def predict_bulk(reviews, progress_callback=None):
    """
    Predict sentiment for multiple reviews.

    Args:
        reviews: list of review texts.
        progress_callback: optional callable(done_count, total_count)
            invoked after each inference batch.

    Returns:
        List with one dict per input review:
            {
                "valid": True/False,
                "prediction": "Negative" | "Neutral" | "Positive" | "Invalid review",
                "confidence": 0.0 - 1.0 (None when invalid),
                "negative": probability,
                "neutral": probability,
                "positive": probability,
            }
    """

    batch_results = predict_batch_with_probabilities(
        reviews,
        progress_callback=progress_callback,
    )

    results = []

    for item in batch_results:

        if item is None:
            results.append(
                {
                    "valid": False,
                    "prediction": "Invalid review",
                    "confidence": None,
                    "negative": None,
                    "neutral": None,
                    "positive": None,
                }
            )

        else:

            label, probabilities = item

            results.append(
                {
                    "valid": True,
                    "prediction": label,
                    "confidence": probabilities[label],
                    "negative": probabilities["Negative"],
                    "neutral": probabilities["Neutral"],
                    "positive": probabilities["Positive"],
                }
            )

    return results
