from app.ml.preprocessing import extract_features
from app.ml.model import load_model
from app.ml.transformer_model import load_transformer
from app.core.config import AI_THRESHOLD, MIN_TEXT_LENGTH
from app.services.decision_service import make_final_decision
from app.services.logging_service import log_analysis


def interpret_confidence(probability: float) -> str:
    if probability >= 0.85:
        return "high"
    elif probability >= 0.65:
        return "medium"
    else:
        return "low"


def analyze_text(text: str):
    # === Validation ===
    words = text.split()
    if len(words) < MIN_TEXT_LENGTH:
        return {
            "error": "Text too short for reliable analysis",
            "min_required_words": MIN_TEXT_LENGTH,
            "provided_words": len(words)
        }

    # === Feature extraction ===
    features = extract_features(text)
    print("CALLING load_model()")

    # === Logistic Regression ===
    lr_model = load_model()
    X = [list(features.values())]

    lr_prob = float(lr_model.predict_proba(X)[0][1])
    lr_label = "AI" if lr_prob >= AI_THRESHOLD else "human"
    lr_confidence = interpret_confidence(lr_prob)

    lr_feedback = (
        "Text structure and statistical features resemble AI-generated content."
        if lr_label == "AI"
        else
        "Statistical features are consistent with human-written text."
    )

    lr_result = {
        "ai_probability": round(lr_prob, 2),
        "label": lr_label,
        "confidence_level": lr_confidence,
        "feedback": lr_feedback
    }

    # === Transformer ===
    transformer = load_transformer()
    t_result = transformer(text[:512])[0]

    t_prob = float(t_result["score"])
    t_label = "AI" if t_result["label"] == "POSITIVE" else "human"
    t_confidence = interpret_confidence(t_prob)

    t_feedback = (
        "Semantic coherence and phrasing patterns suggest AI-generated text."
        if t_label == "AI"
        else
        "Semantic patterns are typical for human-authored text."
    )

    transformer_result = {
        "ai_probability": round(t_prob, 2),
        "label": t_label,
        "confidence_level": t_confidence,
        "feedback": t_feedback
    }

    # === Decision Engine (ensemble logic) ===
    final_decision = make_final_decision(
        lr_result=lr_result,
        transformer_result=transformer_result
    )

    # === Logging to CSV (experiments / evaluation) ===
    log_analysis(
        text=text,
        lr_result=lr_result,
        transformer_result=transformer_result,
        final_decision=final_decision
    )

    # === Final response ===
    return {
        "logistic_regression": lr_result,
        "transformer": transformer_result,
        "final_decision": final_decision,
        "features": features
    }
