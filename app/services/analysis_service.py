from app.ml.preprocessing import extract_features
from app.ml.model import load_model
from app.ml.transformer_model import load_transformer
from app.core.config import AI_THRESHOLD, MIN_TEXT_LENGTH


def analyze_text(text: str):
    # === Validation: minimal text length ===
    word_count = len(text.split())
    if word_count < MIN_TEXT_LENGTH:
        return {
            "error": "Text too short for reliable analysis",
            "min_required_words": MIN_TEXT_LENGTH,
            "provided_words": word_count
        }

    # === Feature extraction ===
    features = extract_features(text)

    # === Logistic Regression ===
    lr_model = load_model()
    X = [list(features.values())]

    lr_prob = float(lr_model.predict_proba(X)[0][1])
    lr_label = "AI" if lr_prob >= AI_THRESHOLD else "human"

    # === Transformer ===
    transformer = load_transformer()
    t_result = transformer(text[:512])[0]  # token limit safety

    t_score = float(t_result["score"])
    t_label = "AI" if t_result["label"] == "POSITIVE" else "human"

    # === Final response ===
    return {
        "logistic_regression": {
            "ai_probability": round(lr_prob, 2),
            "label": lr_label
        },
        "transformer": {
            "ai_probability": round(t_score, 2),
            "label": t_label
        },
        "features": features
    }
