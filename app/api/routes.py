from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Union

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
    confidence: str
    weighted_score: float



class AnalyzeResponse(BaseModel):
    transformer: ModelResult
    logistic_regression: ModelResult
    verdict: Verdict
    features: Dict[str, Union[int, float]]
    explainability: "Explainability"

    class Config:
        extra = "forbid"

class ExplainFeature(BaseModel):
    feature: str
    value: float
    weight: float
    impact: float


class Explainability(BaseModel):
    model_type: str
    top_positive_features: list[ExplainFeature]
    top_negative_features: list[ExplainFeature]
    note: str


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

    return analyze_text(text)
