from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any


# ============================================================================
# REQUEST MODELS
# ============================================================================


class GetAiUsageRequest(BaseModel):
    """Request model for getting AI usage data"""

    skip: int = Field(
        default=0, ge=0, description="Number of records to skip for pagination"
    )
    take: int = Field(
        default=10, ge=1, le=100, description="Number of records to take (max 100)"
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================


class AiUsageData(BaseModel):
    """Core AI usage data model"""

    id: str = Field(description="AI usage record UUID")
    user_id: str = Field(description="UUID of the user who generated the usage")
    cost: float = Field(description="Cost of the AI usage")
    usage: Dict[str, Any] = Field(description="Usage details as JSON")
    metadata: Dict[str, Any] = Field(description="Additional metadata as JSON")
    created_at: datetime = Field(description="When the usage was recorded")
    updated_at: datetime = Field(description="When the usage was last updated")


class AiUsageResponse(BaseModel):
    """Response model for single AI usage operations"""

    status: str = "success"
    ai_usage: AiUsageData
    message: str | None = None


class AiUsageListResponse(BaseModel):
    """Response model for listing AI usage data with pagination"""

    status: str = "success"
    ai_usage_records: list[AiUsageData]
    total_count: int
    skip: int
    take: int
