from app.ml.preprocessing import extract_features
from app.ml.model import load_model
from app.ml.transformer_model import load_transformer
from app.core.config import AI_THRESHOLD, MIN_TEXT_LENGTH
from app.services.decision_service import make_final_decision
from app.services.logging_service import log_analysis
from app.services.explainability_service import explain_lr


def analyze_text(text: str) -> dict:
    # ==============================
    # EDGE CASE: empty input
    # ==============================
    if not text or not text.strip():
        return {
            "error": "Empty text input"
        }

    # ==============================
    # VALIDATION
    # ==============================
    words = text.split()
    if len(words) < MIN_TEXT_LENGTH:
        return {
            "error": "Text too short for reliable analysis",
            "min_required_words": MIN_TEXT_LENGTH,
            "provided_words": len(words),
        }

    # ==============================
    # FEATURE EXTRACTION
    # ==============================
    features = extract_features(text)

    # ==============================
    # LOGISTIC REGRESSION
    # ==============================
    lr_model = load_model()
    X = [list(features.values())]

    lr_prob = float(lr_model.predict_proba(X)[0][1])
    lr_label = "AI" if lr_prob >= AI_THRESHOLD else "human"

    lr_result = {
        "ai_probability": round(lr_prob, 2),
        "label": lr_label,
    }

    # ==============================
    # EXPLAINABILITY (LR)
    # ==============================
    explainability = explain_lr(
        features=features,
        model=lr_model,
        top_k=3
    )

    # ==============================
    # TRANSFORMER (SAFE)
    # ==============================
    transformer = load_transformer()

    try:
        t_result = transformer(text[:512])[0]
        t_prob = float(t_result["score"])
        t_label = "AI" if t_result["label"] == "POSITIVE" else "human"
    except Exception:
        # fallback if transformer fails
        t_prob = 0.5
        t_label = "UNCERTAIN"

    transformer_result = {
        "ai_probability": round(t_prob, 2),
        "label": t_label,
    }

    # ==============================
    # DECISION ENGINE (ENSEMBLE)
    # ==============================
    final_decision = make_final_decision(
        lr_result=lr_result,
        transformer_result=transformer_result
    )

    # ==============================
    # LOGGING (CSV / EXPERIMENTS)
    # ==============================
    log_analysis(
        text=text,
        lr_result=lr_result,
        transformer_result=transformer_result,
        final_decision=final_decision,
    )

    # ==============================
    # API RESPONSE
    # ==============================
    return {
        "logistic_regression": lr_result,
        "transformer": transformer_result,
        "verdict": {
            "label": final_decision["label"],
            "explanation": final_decision["explanation"],
            "confidence": final_decision["confidence"],
            "weighted_score": final_decision["weighted_score"],
        },
        "explainability": explainability,
        "features": features,
    }
