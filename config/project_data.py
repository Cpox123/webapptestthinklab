PROJECT_TITLE = "NLP-based Product Review Sentiment Classification System"

DATASET_NAME = "Women's E-Commerce Clothing Reviews"

LABEL_ORDER = ["Negative", "Neutral", "Positive"]

MAX_SEQUENCE_LENGTH = 128

BULK_ROW_LIMIT = 500

MODEL_RESULTS = {
    "Logistic Regression": {
        "accuracy": 0.7674,
        "macro_f1": 0.6010,
    },
    "LSTM": {
        "accuracy": 0.7022,
        "macro_f1": 0.4408,
    },
    "SVM": {
        "accuracy": 0.8206,
        "macro_f1": 0.5900,
    },
    "BERT": {
        "accuracy": 0.8182,
        "macro_f1": 0.6600,
    },
    "Naive Bayes": {
        "accuracy": 0.7813,
        "macro_f1": 0.5943,
    },
    "CNN": {
        "accuracy": 0.7941,
        "macro_f1": 0.6227,
    },
}

FINAL_MODEL_NAME = "BERT"
