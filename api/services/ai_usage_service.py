from fastapi import HTTPException
from ..databridge.ai_usage_databridge import (
    AiUsageDatabridge,
    DBAiUsageResponse,
    DBAiUsageListResponse,
)
from api.models.v1.ai_usage import (
    AiUsageData,
    AiUsageResponse,
    AiUsageListResponse,
)
from datetime import datetime


class AiUsageService:
    def __init__(self, databridge: AiUsageDatabridge) -> None:
        self.databridge: AiUsageDatabridge = databridge

    def _convert_db_to_model(self, db_ai_usage: DBAiUsageResponse) -> AiUsageData:
        """Convert database response to API model"""
        return AiUsageData(
            id=db_ai_usage.id,
            user_id=db_ai_usage.user_id,
            cost=db_ai_usage.cost,
            usage=db_ai_usage.usage,
            metadata=db_ai_usage.metadata,
            created_at=db_ai_usage.created_at,
            updated_at=db_ai_usage.updated_at,
        )

    async def create_ai_usage_entry(
        self,
        *,
        user_id: str,
        cost: float,
        usage: dict | None = None,
        metadata: dict | None = None,
    ) -> AiUsageData | None:
        """Create an AI usage entry"""
        db_ai_usage = await self.databridge.create_ai_usage_entry(
            user_id=user_id, cost=cost, usage=usage, metadata=metadata
        )
        return (
            self._convert_db_to_model(db_ai_usage=db_ai_usage) if db_ai_usage else None
        )

    async def get_ai_usage_by_id(
        self, *, ai_usage_id: str, user_id: str
    ) -> AiUsageResponse:
        """Get a specific AI usage record by ID for a user"""
        db_ai_usage = await self.databridge.get_ai_usage_by_id(
            ai_usage_id=ai_usage_id, user_id=user_id
        )

        if not db_ai_usage:
            raise HTTPException(status_code=404, detail="AI usage record not found")

        ai_usage_data = self._convert_db_to_model(db_ai_usage)
        return AiUsageResponse(ai_usage=ai_usage_data)

    async def get_user_ai_usage(
        self, *, user_id: str, skip: int = 0, take: int = 10
    ) -> AiUsageListResponse:
        """Get AI usage records for a user with pagination"""
        db_result = await self.databridge.get_user_ai_usage(
            user_id=user_id, skip=skip, take=take
        )

        ai_usage_records = [
            self._convert_db_to_model(record) for record in db_result.ai_usage_records
        ]

        return AiUsageListResponse(
            ai_usage_records=ai_usage_records,
            total_count=db_result.total_count,
            skip=skip,
            take=take,
        )

    async def get_user_ai_usage_by_date_range(
        self,
        *,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        take: int = 10,
    ) -> AiUsageListResponse:
        """Get AI usage records for a user within a date range with pagination"""
        db_result = await self.databridge.get_user_ai_usage_by_date_range(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            take=take,
        )

        ai_usage_records = [
            self._convert_db_to_model(record) for record in db_result.ai_usage_records
        ]

        return AiUsageListResponse(
            ai_usage_records=ai_usage_records,
            total_count=db_result.total_count,
            skip=skip,
            take=take,
        )
