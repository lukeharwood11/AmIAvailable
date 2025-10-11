from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Any


# ============================================================================
# REQUEST MODELS
# ============================================================================


class CreateNotificationRequest(BaseModel):
    """Request model for creating a new notification"""

    title: str = Field(
        description="Notification title",
        examples=["New Event Request"],
        min_length=1,
        max_length=255,
    )
    message: str = Field(
        description="Notification message",
        examples=["You have a new event request that needs approval"],
        min_length=1,
        max_length=1000,
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional payload data for the notification",
        examples=[{"event_request_id": "req-123", "type": "event_request"}],
    )


class UpdateNotificationRequest(BaseModel):
    """Request model for updating a notification"""

    is_read: bool | None = Field(
        None, description="Mark notification as read/unread", examples=[True]
    )
    is_deleted: bool | None = Field(
        None, description="Mark notification as deleted", examples=[False]
    )


class GetNotificationsRequest(BaseModel):
    """Request model for getting notifications"""

    is_read: bool | None = Field(
        None, description="Filter by read status", examples=[False]
    )
    is_deleted: bool | None = Field(
        None, description="Filter by deleted status", examples=[False]
    )
    skip: int = Field(
        default=0, ge=0, description="Number of records to skip for pagination"
    )
    take: int = Field(
        default=50, ge=1, le=100, description="Number of records to take (max 100)"
    )


class MarkAllAsReadRequest(BaseModel):
    """Request model for marking all notifications as read"""

    pass


class DeleteNotificationRequest(BaseModel):
    """Request model for deleting a notification"""

    notification_id: str = Field(
        description="UUID of the notification to delete",
        examples=["notif-123e4567-e89b-12d3-a456-426614174000"],
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================


class NotificationData(BaseModel):
    """Core notification data model"""

    id: str = Field(description="Notification UUID")
    user_id: str = Field(description="UUID of the user who owns the notification")
    title: str = Field(description="Notification title")
    message: str = Field(description="Notification message")
    payload: dict[str, Any] = Field(description="Additional payload data")
    is_read: bool = Field(description="Whether the notification has been read")
    is_deleted: bool = Field(description="Whether the notification has been deleted")
    created_at: datetime = Field(description="When the notification was created")
    updated_at: datetime = Field(description="When the notification was last updated")


class NotificationResponse(BaseModel):
    """Response model for single notification operations"""

    status: str = "success"
    notification: NotificationData
    message: str | None = None


class NotificationsListResponse(BaseModel):
    """Response model for listing notifications"""

    status: str = "success"
    notifications: list[NotificationData]
    count: int
    total_count: int
    skip: int
    take: int
    filters: dict[str, str | bool] | None = None


class NotificationCreateResponse(BaseModel):
    """Response model for notification creation"""

    status: str = "success"
    notification: NotificationData
    message: str = "Notification created successfully"


class NotificationUpdateResponse(BaseModel):
    """Response model for notification updates"""

    status: str = "success"
    notification: NotificationData
    message: str = "Notification updated successfully"


class NotificationDeleteResponse(BaseModel):
    """Response model for notification deletion"""

    status: str = "success"
    message: str = "Notification deleted successfully"


class MarkAllAsReadResponse(BaseModel):
    """Response model for marking all notifications as read"""

    status: str = "success"
    message: str = "All notifications marked as read"
    updated_count: int = Field(description="Number of notifications updated")
