from fastapi import APIRouter
from pydantic import BaseModel
from urllib.parse import urlparse

router = APIRouter()


class URLAnalyzeRequest(BaseModel):
    url: str


@router.post("/analyze")
def analyze_url(payload: URLAnalyzeRequest):
    url = payload.url.strip()

    parsed = urlparse(url)

    suspicious_keywords = [
        "login",
        "verify",
        "verification",
        "account",
        "secure",
        "update",
        "password",
        "signin",
    ]

    lowered = url.lower()

    keyword_hits = [
        keyword for keyword in suspicious_keywords
        if keyword in lowered
    ]

    has_https = parsed.scheme.lower() == "https"
    has_valid_scheme = parsed.scheme.lower() in {"http", "https"}
    has_hostname = bool(parsed.hostname)

    risk_score = 0

    if not has_valid_scheme:
        risk_score += 30

    if not has_hostname:
        risk_score += 30

    if not has_https:
        risk_score += 15

    risk_score += min(len(keyword_hits) * 8, 40)

    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "url": url,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "https": has_https,
        "hostname": parsed.hostname,
        "keyword_indicators": keyword_hits,
    }
