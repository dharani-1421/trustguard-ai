"""Health check routes."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return process liveness. Does not imply ML or database readiness."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="trustguard-ai",
        version=settings.app_version,
        environment=settings.environment,
    )
