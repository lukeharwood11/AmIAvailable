from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DBAiUsageResponse(BaseModel):
    id: str
    user_id: str
    cost: float
    usage: dict
    metadata: dict
    created_at: datetime
    updated_at: datetime


class DBAiUsageListResponse(BaseModel):
    ai_usage_records: list[DBAiUsageResponse]
    total_count: int


class AiUsageDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.ai_usage = self.supabase.table("ai_usage")

    async def get_ai_usage_by_id(
        self, *, ai_usage_id: str, user_id: str
    ) -> DBAiUsageResponse | None:
        """Get a specific AI usage record by ID for a user"""
        try:
            response = (
                self.ai_usage.select("*")
                .eq("id", ai_usage_id)
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBAiUsageResponse(**response.data)
        except Exception as e:
            logger.info(f"Error fetching AI usage by ID: {e}")
            return None

    async def get_user_ai_usage(
        self, *, user_id: str, skip: int = 0, take: int = 10
    ) -> DBAiUsageListResponse:
        """Get AI usage records for a user with pagination"""
        try:
            # Get total count
            count_response = (
                self.ai_usage.select("id", count="exact")
                .eq("user_id", user_id)
                .execute()
            )
            total_count = count_response.count or 0

            # Get paginated records
            response = (
                self.ai_usage.select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .range(skip, skip + take - 1)
                .execute()
            )

            if not response.data:
                return DBAiUsageListResponse(ai_usage_records=[], total_count=0)

            ai_usage_records = [DBAiUsageResponse(**item) for item in response.data]

            return DBAiUsageListResponse(
                ai_usage_records=ai_usage_records, total_count=total_count
            )
        except Exception as e:
            logger.info(f"Error fetching user AI usage: {e}")
            return DBAiUsageListResponse(ai_usage_records=[], total_count=0)

    async def get_user_ai_usage_by_date_range(
        self,
        *,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        take: int = 10,
    ) -> DBAiUsageListResponse:
        """Get AI usage records for a user within a date range with pagination"""
        try:
            # Get total count
            count_response = (
                self.ai_usage.select("id", count="exact")
                .eq("user_id", user_id)
                .gte("created_at", start_date.isoformat())
                .lte("created_at", end_date.isoformat())
                .execute()
            )
            total_count = count_response.count or 0

            # Get paginated records
            response = (
                self.ai_usage.select("*")
                .eq("user_id", user_id)
                .gte("created_at", start_date.isoformat())
                .lte("created_at", end_date.isoformat())
                .order("created_at", desc=True)
                .range(skip, skip + take - 1)
                .execute()
            )

            if not response.data:
                return DBAiUsageListResponse(ai_usage_records=[], total_count=0)

            ai_usage_records = [DBAiUsageResponse(**item) for item in response.data]

            return DBAiUsageListResponse(
                ai_usage_records=ai_usage_records, total_count=total_count
            )
        except Exception as e:
            logger.info(f"Error fetching user AI usage by date range: {e}")
            return DBAiUsageListResponse(ai_usage_records=[], total_count=0)
