from app.core.config import (
    LR_WEIGHT,
    TRANSFORMER_WEIGHT,
    FINAL_AI_THRESHOLD,
    FINAL_HUMAN_THRESHOLD
)


def label_to_score(label: str) -> float:
    return 1.0 if label == "AI" else 0.0


def make_final_decision(lr_result: dict, transformer_result: dict):
    lr_score = label_to_score(lr_result["label"])
    tr_score = label_to_score(transformer_result["label"])

    weighted_score = (
        lr_score * LR_WEIGHT +
        tr_score * TRANSFORMER_WEIGHT
    )

    if weighted_score >= FINAL_AI_THRESHOLD:
        final_label = "AI"
        confidence = "high"
        explanation = "Weighted consensus indicates AI-generated text."

    elif weighted_score <= FINAL_HUMAN_THRESHOLD:
        final_label = "human"
        confidence = "high"
        explanation = "Weighted consensus indicates human-written text."

    else:
        final_label = "uncertain"
        confidence = "medium"
        explanation = (
            "Models provide conflicting signals; classification is uncertain."
        )

    return {
        "final_label": final_label,
        "confidence": confidence,
        "weighted_score": round(weighted_score, 2),
        "explanation": explanation
    }
