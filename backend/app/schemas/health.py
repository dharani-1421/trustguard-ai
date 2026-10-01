from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Process liveness: 'ok' when the API is serving.")
    service: str
    version: str
    environment: str
