from pydantic import BaseModel, Field


class PhishingAnalyzeRequest(BaseModel):
    sender: str = ""
    subject: str = ""
    body: str = Field(min_length=1)


class PhishingAnalyzeResponse(BaseModel):
    prediction: str
    predicted_label: int
    probability: float
    probability_phishing: float
    probability_legitimate: float
    probability_type: str
    model: str
    model_version: str
    explanation: list[dict]
    threat_status: str
    input_used: dict
