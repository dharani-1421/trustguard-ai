from fastapi import APIRouter, HTTPException

from app.schemas.phishing import (
    PhishingAnalyzeRequest,
    PhishingAnalyzeResponse,
)

from ml.phishing.predict import (
    ModelNotTrainedError,
    analyze_email,
)


router = APIRouter()


@router.post("/analyze", response_model=PhishingAnalyzeResponse)
def analyze_phishing(payload: PhishingAnalyzeRequest):
    try:
        result = analyze_email(
            sender=payload.sender,
            subject=payload.subject,
            body=payload.body,
        )
        return result
    except ModelNotTrainedError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
