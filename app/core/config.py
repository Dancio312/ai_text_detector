# Central configuration for evaluation and models

MODEL_NAMES = {
    "logistic_regression": "Logistic Regression",
    "transformer": "Transformer (DistilBERT)"
}

# Decision thresholds
AI_THRESHOLD = 0.6

# Minimum text length (in words) for reliable analysis
MIN_TEXT_LENGTH = 20

# Evaluation settings
EVALUATION_COLUMNS = [
    "lr_probability",
    "lr_label",
    "transformer_probability",
    "transformer_label"
]
