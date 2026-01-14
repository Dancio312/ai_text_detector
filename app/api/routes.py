from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

router = APIRouter()

MIN_WORDS = 20
DEMO_MODE = True  # ← do usunięcia po podpięciu modeli ML


class AnalyzeRequest(BaseModel):
    text: str


@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/analyze")
async def analyze(payload: AnalyzeRequest) -> Dict[str, Any]:
    text = (payload.text or "").strip()
    words = text.split()

    if len(words) < MIN_WORDS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Text too short for reliable analysis",
                "min_required_words": MIN_WORDS,
                "provided_words": len(words),
            },
        )

    # ==============================
    # TRYB DEMO / MOCK (do podpięcia ML)
    # ==============================
    if DEMO_MODE:
        transformer_prob = 0.6
        logistic_prob = 0.4
    else:
        # TODO: Podpiąć rzeczywiste modele ML
        transformer_prob = 0.0
        logistic_prob = 0.0

    return {
        "transformer": {
            "ai_probability": transformer_prob,
            "label": "AI" if transformer_prob >= 0.5 else "HUMAN",
        },
        "logistic_regression": {
            "ai_probability": logistic_prob,
            "label": "AI" if logistic_prob >= 0.5 else "HUMAN",
        },
        "features": {
            "word_count": len(words),
        },
    }
