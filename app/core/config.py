# Central configuration for evaluation and models

MODEL_NAMES = {
    "logistic_regression": "Logistic Regression",
    "transformer": "Transformer (DistilBERT)"
}

# Logistic Regression decision threshold
AI_THRESHOLD = 0.8

# Minimum text length (in words) for reliable analysis
MIN_TEXT_LENGTH = 20

# Evaluation settings
EVALUATION_COLUMNS = [
    "lr_probability",
    "lr_label",
    "transformer_probability",
    "transformer_label"
]

# Decision engine weights
LR_WEIGHT = 0.4
TRANSFORMER_WEIGHT = 0.6

# Final ensemble decision thresholds
FINAL_AI_THRESHOLD = 0.75
FINAL_HUMAN_THRESHOLD = 0.25
