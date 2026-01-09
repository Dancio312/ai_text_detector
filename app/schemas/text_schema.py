from pydantic import BaseModel
from typing import Dict

class ModelResult(BaseModel):
    ai_probability: float
    label: str

class TextRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    logistic_regression: ModelResult
    transformer: ModelResult
    features: Dict[str, float]
