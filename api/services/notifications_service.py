from fastapi import HTTPException
from pydantic import BaseModel
from typing import Literal
from api.databridge.notifications_databridge import (
    NotificationsDatabridge,
    DBNotificationResponse,
)
import api.models.v1.notifications as models
from enum import Enum
from typing import Any


# Types
class NotificationType(Enum):
    EVENT_REQUEST = "event_request"
    RELATIONSHIP = "relationship"


# ============================================================================
# Notification payloads
# ============================================================================


class User(BaseModel):
    id: str
    name: str | None = None
    email: str


class EventRequestNotificationPayload(BaseModel):
    event_request_id: str
    update: Literal["created", "updated", "deleted"] = "created"
    user: User | None = None


class RelationshipNotificationPayload(BaseModel):
    id: str  # relationship_request_id or relationship_id
    update: Literal["created", "accepted"] = "created"
    user: User | None = None


class NotificationsService:
    def __init__(self, databridge: NotificationsDatabridge) -> None:
        self.databridge: NotificationsDatabridge = databridge

    def _convert_db_to_model(
        self, db_notification: DBNotificationResponse
    ) -> models.NotificationData:
        """Convert database response to API model"""
        return models.NotificationData(
            id=db_notification.id,
            user_id=db_notification.user_id,
            title=db_notification.title,
            message=db_notification.message,
            payload=db_notification.payload,
            is_read=db_notification.is_read,
            is_deleted=db_notification.is_deleted,
            created_at=db_notification.created_at,
            updated_at=db_notification.updated_at,
        )

    async def create_event_request_notification(
        self, to_user_id: str, payload: EventRequestNotificationPayload
    ) -> models.NotificationCreateResponse:
        """Create a new event request notification"""
        assert payload.user, "payload.user needs to be set"
        _user_name = (
            f"{payload.user.name} ({payload.user.email})"
            if payload.user.name
            else payload.user.email
        )
        if payload.update == "created":
            title = "New Event Request"
            message = f"{_user_name} has created a new event request."
        elif payload.update == "updated":
            title = "Event Request Updated"
            message = f"{_user_name} has updated their event request."
        elif payload.update == "deleted":
            title = "Event Request Deleted"
            message = f"{_user_name} has deleted their event request."
        else:
            raise ValueError("Invalid update type")
        return await self.create_notification(
            user_id=to_user_id,
            title=title,
            message=message,
            payload=payload.model_dump(),
        )

    async def create_relationship_notification(
        self, to_user_id: str, payload: RelationshipNotificationPayload
    ) -> models.NotificationCreateResponse:
        """Create a new relationship notification"""
        assert payload.user, "payload.user needs to be set"
        _user_name = (
            f"{payload.user.name} ({payload.user.email})"
            if payload.user.name
            else payload.user.email
        )
        if payload.update == "created":
            title = f"New Relationship Request"
            message = f"{_user_name} would like to add you as a connection."
        elif payload.update == "accepted":
            title = f"Relationship Request Accepted"
            message = f"{_user_name} has accepted your connection request."
        else:
            raise ValueError("Invalid update type")
        return await self.create_notification(
            user_id=to_user_id,
            title=title,
            message=message,
            payload=payload.model_dump(),
        )

    async def create_notification(
        self,
        *,
        user_id: str,
        title: str,
        message: str,
        payload: dict[str, Any] | None = None,
    ) -> models.NotificationCreateResponse:
        """Create a new notification"""
        # Validate input
        if not title or not title.strip():
            raise HTTPException(status_code=400, detail="Title is required")
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Message is required")

        # Create the notification
        db_notification = await self.databridge.create_notification(
            user_id=user_id,
            title=title.strip(),
            message=message.strip(),
            payload=payload or {},
        )

        if not db_notification:
            raise HTTPException(
                status_code=500, detail="Failed to create notification")

        notification_data = self._convert_db_to_model(db_notification)
        return models.NotificationCreateResponse(notification=notification_data)

    async def get_notification(
        self, *, notification_id: str, user_id: str
    ) -> models.NotificationResponse:
        """Get a specific notification by ID"""
        db_notification = await self.databridge.get_notification_by_id(
            notification_id=notification_id
        )

        if not db_notification:
            raise HTTPException(
                status_code=404, detail="Notification not found")

        # Check if user has permission to view this notification
        if db_notification.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to view this notification",
            )

        notification_data = self._convert_db_to_model(db_notification)
        return models.NotificationResponse(notification=notification_data)

    async def get_user_notifications(
        self,
        *,
        user_id: str,
        is_read: bool | None = None,
        is_deleted: bool | None = None,
        skip: int = 0,
        take: int = 50,
    ) -> models.NotificationsListResponse:
        """Get notifications for a user with optional filters and pagination"""
        # Validate pagination parameters
        if skip < 0:
            raise HTTPException(
                status_code=400, detail="Skip must be non-negative")
        if take < 1 or take > 100:
            raise HTTPException(
                status_code=400, detail="Take must be between 1 and 100"
            )

        db_result = await self.databridge.get_user_notifications(
            user_id=user_id,
            is_read=is_read,
            is_deleted=is_deleted,
            skip=skip,
            take=take,
        )

        notifications = [
            self._convert_db_to_model(notif) for notif in db_result.notifications
        ]

        filters: dict[str, bool] = {}
        if is_read is not None:
            filters["is_read"] = is_read
        if is_deleted is not None:
            filters["is_deleted"] = is_deleted

        return models.NotificationsListResponse(
            notifications=notifications,
            count=len(notifications),
            total_count=db_result.total_count,
            skip=skip,
            take=take,
            filters=filters if filters else None,
        )

    async def update_notification(
        self,
        *,
        notification_id: str,
        user_id: str,
        is_read: bool | None = None,
        is_deleted: bool | None = None,
    ) -> models.NotificationUpdateResponse:
        """Update a notification"""
        # First verify the notification exists and user has permission
        existing = await self.databridge.get_notification_by_id(
            notification_id=notification_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Notification not found")

        # Check if user has permission to update this notification
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this notification",
            )

        # Update the notification
        db_notification = await self.databridge.update_notification(
            notification_id=notification_id,
            is_read=is_read,
            is_deleted=is_deleted,
        )

        if not db_notification:
            raise HTTPException(
                status_code=500, detail="Failed to update notification")

        notification_data = self._convert_db_to_model(db_notification)
        return models.NotificationUpdateResponse(notification=notification_data)

    async def delete_notification(
        self, *, notification_id: str, user_id: str
    ) -> models.NotificationDeleteResponse:
        """Delete a notification"""
        # First verify the notification exists and user has permission
        existing = await self.databridge.get_notification_by_id(
            notification_id=notification_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Notification not found")

        # Check if user has permission to delete this notification
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this notification",
            )

        # Delete the notification
        success = await self.databridge.delete_notification(
            notification_id=notification_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete notification")

        return models.NotificationDeleteResponse()

    async def mark_all_as_read(self, *, user_id: str) -> models.MarkAllAsReadResponse:
        """Mark all notifications as read for a user"""
        updated_count = await self.databridge.mark_all_as_read(user_id=user_id)
        return models.MarkAllAsReadResponse(updated_count=updated_count)
