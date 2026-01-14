from app.core.config import (
    LR_WEIGHT,
    TRANSFORMER_WEIGHT,
    FINAL_AI_THRESHOLD,
    FINAL_HUMAN_THRESHOLD,
)


def interpret_confidence(score: float) -> str:
    if score >= 0.85:
        return "high"
    elif score >= 0.65:
        return "medium"
    else:
        return "low"


def make_final_decision(lr_result: dict, transformer_result: dict) -> dict:
    lr_prob = lr_result["ai_probability"]
    t_prob = transformer_result["ai_probability"]

    weighted_score = (
        lr_prob * LR_WEIGHT +
        t_prob * TRANSFORMER_WEIGHT
    )

    if weighted_score >= FINAL_AI_THRESHOLD:
        label = "AI"
        explanation = (
            "Weighted ensemble score exceeds AI threshold. "
            "Both semantic and statistical signals indicate AI-generated text."
        )

    elif weighted_score <= FINAL_HUMAN_THRESHOLD:
        label = "HUMAN"
        explanation = (
            "Weighted ensemble score is below human threshold. "
            "The text is consistent with human-authored content."
        )

    else:
        label = "UNCERTAIN"
        explanation = (
            "Models provide conflicting or weak signals. "
            "Classification confidence is insufficient."
        )

    return {
        "label": label,
        "confidence": interpret_confidence(weighted_score),
        "weighted_score": round(weighted_score, 3),
        "explanation": explanation,
    }
