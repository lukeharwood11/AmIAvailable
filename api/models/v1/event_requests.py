from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
from typing import Literal
import api.models.v1.event_request_approvals as era_models


# ============================================================================
# DATE MODELS
# ============================================================================


class EventDateTime(BaseModel):
    """Represents date/time information matching Google API format"""

    date: str | None = Field(
        None,
        description="Date in YYYY-MM-DD format for all-day events",
        examples=["2024-01-15"],
    )
    date_time: datetime | None = Field(
        None,
        description="Date and time for timed events",
        examples=["2024-01-15T14:30:00"],
    )
    time_zone: str | None = Field(
        None, description="Time zone identifier", examples=["America/New_York"]
    )


# ============================================================================
# REQUEST MODELS
# ============================================================================


class CreateEventRequestRequest(BaseModel):
    """Request model for creating a new event request"""

    google_event_id: str | None = Field(
        None,
        description="Google Calendar event ID if created from Google Calendar",
        examples=["abc123def456"],
    )
    title: str | None = Field(
        None, description="Event title", examples=["Team Meeting"]
    )
    location: str | None = Field(
        None, description="Event location", examples=["Conference Room A"]
    )
    description: str | None = Field(
        None,
        description="Event description",
        examples=["Weekly team sync to discuss project progress"],
    )
    start_date: EventDateTime = Field(
        description="Event start date and time, use date_time if time is given, otherwise use date (example: 2024-01-15)",
        examples=[
            {"date_time": "2024-01-15T14:30:00", "time_zone": "America/New_York"}
        ],
    )
    end_date: EventDateTime = Field(
        description="Event end date and time",
        examples=[
            {"date_time": "2024-01-15T15:30:00", "time_zone": "America/New_York"}
        ],
    )
    importance_level: int = Field(
        1,
        ge=1,
        le=5,
        description="Importance level from 1 (low) to 5 (critical)",
        examples=[3],
    )
    notes: str | None = Field(
        None,
        description="Additional notes for the event",
        examples=["Please bring your laptops"],
    )
    approvers: list[era_models.EventRequestApprovalUser] | None = Field(
        default_factory=list,
        description="List of user IDs that are approvers",
        examples=[[{"user_id": "user-123", "required": True}]],
    )


class SmartParseEventRequestRequest(CreateEventRequestRequest):
    current_date: datetime = Field(
        description="Current date with timezone",
        examples=[datetime.now(timezone(timedelta(hours=-5)))],
    )


class UpdateEventRequestRequest(BaseModel):
    """Request model for updating an event request"""

    event_request_id: str = Field(
        description="UUID of the event request to update",
        examples=["req-123e4567-e89b-12d3-a456-426614174000"],
    )
    google_event_id: str | None = Field(
        None, description="Google Calendar event ID", examples=["abc123def456"]
    )
    title: str | None = Field(
        None, description="Updated event title", examples=["Updated Team Meeting"]
    )
    location: str | None = Field(
        None, description="Updated event location", examples=["Conference Room B"]
    )
    description: str | None = Field(
        None,
        description="Updated event description",
        examples=["Updated weekly team sync"],
    )
    start_date: EventDateTime | None = Field(
        None,
        description="Updated event start date and time",
        examples=[
            {"date_time": "2024-01-15T15:00:00", "time_zone": "America/New_York"}
        ],
    )
    end_date: EventDateTime | None = Field(
        None,
        description="Updated event end date and time",
        examples=[
            {"date_time": "2024-01-15T16:00:00", "time_zone": "America/New_York"}
        ],
    )
    importance_level: int | None = Field(
        None, ge=1, le=5, description="Updated importance level", examples=[4]
    )
    status: Literal["pending", "approved", "rejected"] | None = Field(
        None, description="Updated event request status", examples=["approved"]
    )
    notes: str | None = Field(
        None, description="Updated notes", examples=["Updated notes for the meeting"]
    )


class GetEventRequestsRequest(BaseModel):
    """Request model for getting event requests"""

    status: Literal["pending", "approved", "rejected"] | None = Field(
        None, description="Filter by event request status", examples=["pending"]
    )
    importance_level: int | None = Field(
        None, ge=1, le=5, description="Filter by importance level", examples=[3]
    )
    start_date_from: EventDateTime | None = Field(
        None,
        description="Filter events starting from this date",
        examples=[
            {"date_time": "2024-01-01T00:00:00", "time_zone": "America/New_York"}
        ],
    )
    start_date_to: EventDateTime | None = Field(
        None,
        description="Filter events starting before this date",
        examples=[
            {"date_time": "2024-12-31T23:59:59", "time_zone": "America/New_York"}
        ],
    )
    created_by: str | None = Field(
        None,
        description="Filter by creator user ID",
        examples=["user-123e4567-e89b-12d3-a456-426614174000"],
    )


class ListEventRequestsWithApprovalsRequest(BaseModel):
    """Request model for listing event requests with approval status"""

    status: Literal["pending", "approved", "rejected"] | None = Field(
        None, description="Filter by event request status", examples=["pending"]
    )
    skip: int = Field(
        0, ge=0, description="Number of records to skip for pagination", examples=[0]
    )
    take: int = Field(
        50,
        ge=1,
        le=100,
        description="Number of records to return (max 100)",
        examples=[25],
    )


class DeleteEventRequestRequest(BaseModel):
    """Request model for deleting an event request"""

    event_request_id: str = Field(
        description="UUID of the event request to delete",
        examples=["req-123e4567-e89b-12d3-a456-426614174000"],
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================


class SmartParseEvent(BaseModel):
    """Model for smart parse event"""

    title: str | None = Field(
        None, description="Event title", examples=["Team Meeting"]
    )
    location: str | None = Field(
        None, description="Event location", examples=["Conference Room A"]
    )
    description: str | None = Field(
        None,
        description="Event description",
        examples=["Weekly team sync to discuss project progress"],
    )
    start_date: EventDateTime = Field(
        description="Event start date and time, use date_time if time is given, otherwise use date (example: 2024-01-15)",
        examples=[
            {"date_time": "2024-01-15T14:30:00", "time_zone": "America/New_York"}
        ],
    )
    end_date: EventDateTime = Field(
        description="Event end date and time",
        examples=[
            {"date_time": "2024-01-15T15:30:00", "time_zone": "America/New_York"}
        ],
    )
    importance_level: int = Field(
        1,
        ge=1,
        le=5,
        description="Importance level from 1 (low) to 5 (critical)",
        examples=[3],
    )
    notes: str | None = Field(
        None,
        description="Additional notes for the event",
        examples=["Please bring your laptops"],
    )
    approvers: list[era_models.EventRequestApprovalUser] | None = Field(
        default_factory=list,
        description="List of user IDs that are approvers",
        examples=[[{"user_id": "user-123", "required": True}]],
    )


class SmartParseEventRequestResponse(BaseModel):
    """Response model for smart parse event request"""

    status: str = "success"
    event_request: SmartParseEvent
    message: str = "Event request parsed successfully"


class EventRequestData(BaseModel):
    """Core event request data model"""

    id: str = Field(description="Event request UUID")
    google_event_id: str | None = Field(description="Google Calendar event ID")
    title: str | None = Field(description="Event title")
    location: str | None = Field(description="Event location")
    description: str | None = Field(description="Event description")
    start_date: EventDateTime = Field(description="Event start date and time")
    end_date: EventDateTime = Field(description="Event end date and time")
    importance_level: int = Field(description="Importance level from 1 to 5")
    status: str = Field(description="Event request status")
    notes: str | None = Field(description="Additional notes")
    created_by: str = Field(description="UUID of the user who created the request")
    created_at: datetime = Field(description="When the request was created")
    updated_at: datetime = Field(description="When the request was last updated")


class EventRequestWithApprovalsData(BaseModel):
    """Event request data model with approval status information"""

    id: str = Field(description="Event request UUID")
    google_event_id: str | None = Field(description="Google Calendar event ID")
    title: str | None = Field(description="Event title")
    location: str | None = Field(description="Event location")
    description: str | None = Field(description="Event description")
    start_date: EventDateTime = Field(description="Event start date and time")
    end_date: EventDateTime = Field(description="Event end date and time")
    importance_level: int = Field(description="Importance level from 1 to 5")
    status: str = Field(description="Event request status")
    notes: str | None = Field(description="Additional notes")
    created_by: str = Field(description="UUID of the user who created the request")
    created_at: datetime = Field(description="When the request was created")
    updated_at: datetime = Field(description="When the request was last updated")
    approval_status: str = Field(
        description="Aggregated approval status: pending, approved, rejected, or no_approvals"
    )
    requested_approvals: int = Field(description="Total number of approval requests")
    completed_count: int = Field(
        description="Number of completed (non-pending) approvals"
    )


class EventRequestApprovalData(BaseModel):
    """Event request approval data model"""

    id: str = Field(description="Approval UUID")
    event_request_id: str = Field(description="UUID of the event request")
    user_id: str = Field(description="UUID of the user who needs to approve")
    required: bool = Field(description="Whether this approval is required")
    status: str = Field(description="Approval status")
    response_notes: str | None = Field(description="Notes from the approver")
    responded_at: datetime | None = Field(description="When the user responded")
    created_at: datetime = Field(description="When the approval was created")
    updated_at: datetime = Field(description="When the approval was last updated")


class EventRequestWithApproversData(BaseModel):
    """Event request data model with detailed approvers information"""

    id: str = Field(description="Event request UUID")
    google_event_id: str | None = Field(description="Google Calendar event ID")
    title: str | None = Field(description="Event title")
    location: str | None = Field(description="Event location")
    description: str | None = Field(description="Event description")
    start_date: EventDateTime = Field(description="Event start date and time")
    end_date: EventDateTime = Field(description="Event end date and time")
    importance_level: int = Field(description="Importance level from 1 to 5")
    status: str = Field(description="Event request status")
    notes: str | None = Field(description="Additional notes")
    created_by: str = Field(description="UUID of the user who created the request")
    created_at: datetime = Field(description="When the request was created")
    updated_at: datetime = Field(description="When the request was last updated")
    approvers: list[EventRequestApprovalData] = Field(
        description="List of all approvers and their approval data"
    )


class EventRequestResponse(BaseModel):
    """Response model for single event request operations"""

    status: str = "success"
    event_request: EventRequestData
    message: str | None = None


class EventRequestsListResponse(BaseModel):
    """Response model for listing event requests"""

    status: str = "success"
    event_requests: list[EventRequestData]
    count: int
    filters: dict[str, str | int | EventDateTime] | None = None


class EventRequestsWithApprovalsListResponse(BaseModel):
    """Response model for listing event requests with approval status"""

    status: str = "success"
    event_requests: list[EventRequestWithApprovalsData]
    count: int
    total_count: int
    skip: int
    take: int
    filters: dict[str, str | int] | None = None


class EventRequestDeleteResponse(BaseModel):
    """Response model for event request deletion"""

    status: str = "success"
    message: str = "Event request deleted successfully"


class EventRequestCreateResponse(BaseModel):
    """Response model for event request creation"""

    status: str = "success"
    event_request: EventRequestData
    message: str = "Event request created successfully"


class EventRequestUpdateResponse(BaseModel):
    """Response model for event request updates"""

    status: str = "success"
    event_request: EventRequestData
    message: str = "Event request updated successfully"


class EventRequestWithApproversResponse(BaseModel):
    """Response model for event request with approvers"""

    status: str = "success"
    event_request: EventRequestWithApproversData
    message: str | None = None
