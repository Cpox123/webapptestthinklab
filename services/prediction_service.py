import os

# Must be set before importing TensorFlow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import streamlit as st
import tensorflow as tf
import gdown

from transformers import (
    BertConfig,
    TFBertForSequenceClassification,
    BertTokenizer,
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_PATH = "models/tf_model.h5"

# Google Drive file ID for the trained BERT model
MODEL_FILE_ID = "1JvmGJPC0Xr7qTK1eZxkXP0zjrD-aD64P"

LABELS = [
    "Negative",
    "Neutral",
    "Positive",
]

MAX_SEQUENCE_LENGTH = 128

# Normal inference batch size.
# 32 gives good throughput while remaining reasonable for a small
# deployment environment.
BATCH_SIZE = 32

# If the deployment environment cannot handle 32 reviews at once,
# inference automatically falls back to smaller batches.
MIN_BATCH_SIZE = 4


# --------------------------------------------------
# Download model if it does not exist
# --------------------------------------------------

def _download_model():
    """Download the trained BERT model only when necessary."""

    os.makedirs("models", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        return

    print("Downloading BERT model...")
    print("This may take a few minutes.")

    url = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"

    gdown.download(
        url,
        MODEL_PATH,
        quiet=False,
    )

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "The BERT model could not be downloaded."
        )

    print("BERT model downloaded successfully.")


# --------------------------------------------------
# Cached model and tokenizer
# --------------------------------------------------

@st.cache_resource(show_spinner="Loading BERT sentiment model...")
def _load_model_and_tokenizer():
    """
    Load the BERT model and tokenizer once per Streamlit process.

    Streamlit reruns the application script frequently. Using
    cache_resource prevents the expensive model construction and
    weight loading from happening repeatedly.
    """

    _download_model()

    config = BertConfig.from_pretrained(
        "bert-base-uncased",
        num_labels=3,
    )

    model = TFBertForSequenceClassification(config)

    # Build the model before loading the trained weights.
    dummy_input = {
        "input_ids": tf.zeros(
            (1, MAX_SEQUENCE_LENGTH),
            dtype=tf.int32,
        ),
        "attention_mask": tf.ones(
            (1, MAX_SEQUENCE_LENGTH),
            dtype=tf.int32,
        ),
        "token_type_ids": tf.zeros(
            (1, MAX_SEQUENCE_LENGTH),
            dtype=tf.int32,
        ),
    }

    model(dummy_input, training=False)

    # Load the trained weights.
    model.load_weights(MODEL_PATH)

    # Inference only. The model is never trained by the web app.
    model.trainable = False

    tokenizer = BertTokenizer.from_pretrained(
        "bert-base-uncased"
    )

    return model, tokenizer


# --------------------------------------------------
# Get cached resources
# --------------------------------------------------

model, tokenizer = _load_model_and_tokenizer()


# --------------------------------------------------
# One batch inference
# --------------------------------------------------

def _predict_batch(chunk_texts):
    """
    Run one inference batch.

    Returns:
        NumPy array containing probabilities for each review.
    """

    inputs = tokenizer(
        chunk_texts,
        return_tensors="tf",
        padding=True,
        truncation=True,
        max_length=MAX_SEQUENCE_LENGTH,
    )

    outputs = model(
        inputs,
        training=False,
    )

    return tf.nn.softmax(
        outputs.logits,
        axis=-1,
    ).numpy()


# --------------------------------------------------
# Batch prediction with automatic memory fallback
# --------------------------------------------------

def predict_batch_with_probabilities(
    reviews,
    progress_callback=None,
):
    """
    Predict sentiments for a list of reviews using batched inference.

    Empty or whitespace-only reviews are returned as None.

    If the deployment environment cannot handle the normal batch
    size, the batch is automatically reduced to avoid failing the
    entire prediction operation.
    """

    texts = [
        str(review).strip() if review is not None else ""
        for review in reviews
    ]

    results = [None] * len(texts)

    valid_indices = [
        index
        for index, text in enumerate(texts)
        if text
    ]

    valid_texts = [
        texts[index]
        for index in valid_indices
    ]

    total = len(valid_texts)

    if total == 0:
        return results

    start = 0
    current_batch_size = BATCH_SIZE

    while start < total:

        end = min(
            start + current_batch_size,
            total,
        )

        chunk_texts = valid_texts[start:end]
        chunk_indices = valid_indices[start:end]

        try:
            batch_probabilities = _predict_batch(
                chunk_texts
            )

        except tf.errors.ResourceExhaustedError:
            # Reduce the batch size if the deployment environment
            # runs out of memory.
            if current_batch_size <= MIN_BATCH_SIZE:
                raise

            current_batch_size = max(
                MIN_BATCH_SIZE,
                current_batch_size // 2,
            )

            print(
                "BERT batch was too large. "
                f"Retrying with batch size {current_batch_size}."
            )

            continue

        for position, probabilities in enumerate(
            batch_probabilities
        ):
            index = chunk_indices[position]

            predicted_index = int(
                probabilities.argmax()
            )

            results[index] = (
                LABELS[predicted_index],
                {
                    label: float(probability)
                    for label, probability in zip(
                        LABELS,
                        probabilities,
                    )
                },
            )

        processed = end

        if progress_callback is not None:
            progress_callback(
                processed,
                total,
            )

        start = end

    return results


# --------------------------------------------------
# Cached single prediction
# --------------------------------------------------

@st.cache_data(max_entries=128)
def predict_with_probabilities(review):
    """
    Predict the sentiment of one review.

    A small cache avoids repeating BERT inference when the
    same review is submitted again.
    """

    if not review or not str(review).strip():
        return None

    clean_review = str(review).strip()

    return predict_batch_with_probabilities(
        [clean_review]
    )[0]


# --------------------------------------------------
# Single prediction (label only)
# --------------------------------------------------

def predict_sentiment(review):
    """
    Predict the sentiment of a single review.

    Returns:
        Negative, Neutral, or Positive
    """

    prediction = predict_with_probabilities(review)

    if prediction is None:
        return None

    label, _ = prediction

    return label
