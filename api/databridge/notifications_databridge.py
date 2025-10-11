from api.settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
from typing import Any
import logging

logger = logging.getLogger(__name__)


class DBNotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    payload: dict[str, Any]
    is_read: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class DBNotificationsListResponse(BaseModel):
    notifications: list[DBNotificationResponse]
    total_count: int


class NotificationsDatabridge:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.notifications = self.supabase.table("notifications")

    async def create_notification(
        self,
        *,
        user_id: str,
        title: str,
        message: str,
        payload: dict[str, Any] | None = None,
    ) -> DBNotificationResponse | None:
        """Create a new notification"""
        try:
            data = {
                "user_id": user_id,
                "title": title,
                "message": message,
                "payload": payload or {},
            }

            response = self.notifications.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBNotificationResponse(**_data)
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None

    async def get_notification_by_id(
        self, *, notification_id: str
    ) -> DBNotificationResponse | None:
        """Get a specific notification by ID"""
        try:
            response = (
                self.notifications.select("*").eq("id", notification_id).execute()
            )
            if not response.data or len(response.data) == 0:
                return None

            # Return the first (and should be only) result
            return DBNotificationResponse(**response.data[0])
        except Exception as e:
            logger.error(f"Error fetching notification: {e}")
            return None

    async def get_user_notifications(
        self,
        *,
        user_id: str,
        is_read: bool | None = None,
        is_deleted: bool | None = None,
        skip: int = 0,
        take: int = 50,
    ) -> DBNotificationsListResponse:
        """Get notifications for a user with optional filters and pagination"""
        try:
            query = self.notifications.select("*").eq("user_id", user_id)

            # Apply filters
            if is_read is not None:
                query = query.eq("is_read", is_read)
            if is_deleted is not None:
                query = query.eq("is_deleted", is_deleted)

            # Apply pagination
            query = query.range(skip, skip + take - 1).order("created_at", desc=True)

            response = query.execute()
            if not response.data:
                return DBNotificationsListResponse(notifications=[], total_count=0)

            notifications = [DBNotificationResponse(**item) for item in response.data]

            # Get total count with same filters
            count_query = self.notifications.select("id", count="exact").eq(
                "user_id", user_id
            )
            if is_read is not None:
                count_query = count_query.eq("is_read", is_read)
            if is_deleted is not None:
                count_query = count_query.eq("is_deleted", is_deleted)

            count_response = count_query.execute()
            total_count = count_response.count if count_response.count else 0

            return DBNotificationsListResponse(
                notifications=notifications, total_count=total_count
            )
        except Exception as e:
            logger.error(f"Error fetching user notifications: {e}")
            return DBNotificationsListResponse(notifications=[], total_count=0)

    async def update_notification(
        self,
        *,
        notification_id: str,
        is_read: bool | None = None,
        is_deleted: bool | None = None,
    ) -> DBNotificationResponse | None:
        """Update a notification"""
        try:
            update_data: dict[str, str | bool] = {
                "updated_at": datetime.now().isoformat()
            }

            if is_read is not None:
                update_data["is_read"] = is_read
            if is_deleted is not None:
                update_data["is_deleted"] = is_deleted

            response = (
                self.notifications.update(update_data)
                .eq("id", notification_id)
                .execute()
            )
            if not response.data:
                return None

            return DBNotificationResponse(**response.data[0])
        except Exception as e:
            logger.error(f"Error updating notification: {e}")
            return None

    async def delete_notification(self, *, notification_id: str) -> bool:
        """Delete a notification"""
        try:
            response = self.notifications.delete().eq("id", notification_id).execute()
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            logger.error(f"Error deleting notification: {e}")
            return False

    async def mark_all_as_read(self, *, user_id: str) -> int:
        """Mark all notifications as read for a user"""
        try:
            response = (
                self.notifications.update(
                    {"is_read": True, "updated_at": datetime.now().isoformat()}
                )
                .eq("user_id", user_id)
                .eq("is_read", False)
                .execute()
            )
            return len(response.data) if response.data else 0
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return 0
