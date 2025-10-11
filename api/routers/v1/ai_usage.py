from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from api.settings.auth import get_current_user_id
from api.dependencies import get_ai_usage_service
from api.services.ai_usage_service import AiUsageService
from api.models.v1.ai_usage import (
    AiUsageResponse,
    AiUsageListResponse,
    AiUsageCostResponse,
)


router = APIRouter(prefix="/ai-usage", tags=["AI Usage"])


@router.get("", response_model=AiUsageListResponse)
async def get_user_ai_usage(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    take: int = Query(
        10, ge=1, le=100, description="Number of records to take (max 100)"
    ),
    user_id: str = Depends(get_current_user_id),
    service: AiUsageService = Depends(get_ai_usage_service),
) -> AiUsageListResponse:
    """
    Get AI usage records for the current user with pagination

    Returns:
        List of user's AI usage records with pagination details
    """
    return await service.get_user_ai_usage(
        user_id=user_id,
        skip=skip,
        take=take,
    )

@router.get("/cost")
async def get_user_ai_cost(
    start_date: datetime = Query(
        ..., description="Start date for the range (ISO format)", alias="startDate"
    ),
    end_date: datetime = Query(
        ..., description="End date for the range (ISO format)", alias="endDate"
    ),
    user_id: str = Depends(get_current_user_id),
    service: AiUsageService = Depends(get_ai_usage_service),
) -> AiUsageCostResponse:
    """
    Get AI usage cost for the current user within a date range

    Returns:
        AI usage cost for the current user within a date range
    """
    _cost = await service.get_user_cost_by_date_range(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    return AiUsageCostResponse(
        start_date=start_date,
        end_date=end_date,
        cost=_cost,
    )


@router.get("/{ai_usage_id}", response_model=AiUsageResponse)
async def get_ai_usage_by_id(
    ai_usage_id: str,
    user_id: str = Depends(get_current_user_id),
    service: AiUsageService = Depends(get_ai_usage_service),
) -> AiUsageResponse:
    """
    Get a specific AI usage record by ID for the current user

    Returns:
        AI usage record data
    """
    return await service.get_ai_usage_by_id(ai_usage_id=ai_usage_id, user_id=user_id)


@router.get("/by-date-range", response_model=AiUsageListResponse)
async def get_user_ai_usage_by_date_range(
    start_date: datetime = Query(
        ..., description="Start date for the range (ISO format)"
    ),
    end_date: datetime = Query(..., description="End date for the range (ISO format)"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    take: int = Query(
        10, ge=1, le=100, description="Number of records to take (max 100)"
    ),
    user_id: str = Depends(get_current_user_id),
    service: AiUsageService = Depends(get_ai_usage_service),
) -> AiUsageListResponse:
    """
    Get AI usage records for the current user within a date range with pagination

    Returns:
        List of user's AI usage records within the specified date range with pagination details
    """
    if start_date >= end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )

    return await service.get_user_ai_usage_by_date_range(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        take=take,
    )
