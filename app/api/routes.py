from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

router = APIRouter()

MIN_WORDS = 20


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

    # TODO: tutaj podłączysz swoje modele ML
    return {
        "logistic_regression": {"ai_probability": 0.5, "label": "unknown"},
        "transformer": {"ai_probability": 0.5, "label": "unknown"},
        "features": {"word_count": len(words)},
    }
