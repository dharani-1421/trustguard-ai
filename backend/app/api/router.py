"""API routers."""

from fastapi import APIRouter

from app.api.routes import health, phishing, url_risk

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(phishing.router, prefix="/phishing", tags=["phishing"])
api_router.include_router(url_risk.router, prefix="/url", tags=["url-risk"])
