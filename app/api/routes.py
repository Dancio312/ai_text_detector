from fastapi import APIRouter
from app.schemas.text_schema import TextRequest, AnalysisResponse
from app.services.analysis_service import analyze_text

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: TextRequest):
    return analyze_text(request.text)
