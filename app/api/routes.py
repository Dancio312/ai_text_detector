from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

router = APIRouter()

# ==============================
# CONFIG
# ==============================

MIN_WORDS = 20
DEMO_MODE = True


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

    if word_count < MIN_WORDS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Text too short for reliable analysis",
                "min_required_words": MIN_WORDS,
                "provided_words": word_count,
            },
        )

    # ==============================
    # DEMO MODE
    # ==============================
    if DEMO_MODE:
        transformer_prob = 0.60
        logistic_prob = 0.70
    else:
        transformer_prob = 0.0
        logistic_prob = 0.0

    transformer_label = "AI" if transformer_prob >= 0.5 else "HUMAN"
    logistic_label = "AI" if logistic_prob >= 0.5 else "HUMAN"

    # ==============================
    # FINAL VERDICT
    # ==============================
    if transformer_label == logistic_label:
        verdict_label = transformer_label
        explanation = (
            "Both models independently reached the same conclusion."
        )
    else:
        verdict_label = "UNCERTAIN"
        explanation = (
            "The models produced conflicting predictions, "
            "therefore a definitive classification is not possible."
        )

    return AnalyzeResponse(
        transformer=ModelResult(
            ai_probability=transformer_prob,
            label=transformer_label,
        ),
        logistic_regression=ModelResult(
            ai_probability=logistic_prob,
            label=logistic_label,
        ),
        verdict=Verdict(
            label=verdict_label,
            explanation=explanation,
        ),
        features={
            "word_count": word_count,
        },
    )
