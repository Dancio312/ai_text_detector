from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

router = APIRouter()

# ==============================
# CONFIG
# ==============================

MIN_WORDS = 20
DEMO_MODE = True  # TODO: disable after ML integration


# ==============================
# REQUEST / RESPONSE MODELS
# ==============================

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ModelResult(BaseModel):
    ai_probability: float
    label: str


class AnalyzeResponse(BaseModel):
    transformer: ModelResult
    logistic_regression: ModelResult
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
    # DEMO / MOCK MODE
    # ==============================
    if DEMO_MODE:
        transformer_prob = 0.60
        logistic_prob = 0.40

    # ==============================
    # REAL ML MODE (future)
    # ==============================
    else:
        # TODO:
        # - preprocess text
        # - run transformer model
        # - run classical ML model
        transformer_prob = 0.0
        logistic_prob = 0.0

    transformer_label = "AI" if transformer_prob >= 0.5 else "HUMAN"
    logistic_label = "AI" if logistic_prob >= 0.5 else "HUMAN"

    return AnalyzeResponse(
        transformer=ModelResult(
            ai_probability=transformer_prob,
            label=transformer_label,
        ),
        logistic_regression=ModelResult(
            ai_probability=logistic_prob,
            label=logistic_label,
        ),
        features={
            "word_count": word_count,
        },
    )
