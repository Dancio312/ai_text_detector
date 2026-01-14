from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

from app.services.analysis_service import analyze_text
from app.core.config import MIN_TEXT_LENGTH

router = APIRouter()

# ==============================
# REQUEST / RESPONSE MODELS
# ==============================

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ModelResult(BaseModel):
    ai_probability: float
    label: str


class Verdict(BaseModel):
    label: str
    explanation: str


class AnalyzeResponse(BaseModel):
    transformer: ModelResult
    logistic_regression: ModelResult
    verdict: Verdict
    features: Dict[str, int]


# ==============================
# ROUTES
# ==============================

@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    text = payload.text.strip()
    words = text.split()
    word_count = len(words)

    if word_count < MIN_TEXT_LENGTH:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Text too short for reliable analysis",
                "min_required_words": MIN_TEXT_LENGTH,
                "provided_words": word_count,
            },
        )

    # === REAL ANALYSIS (NO DEMO MODE) ===
    result = analyze_text(text)
    return result
