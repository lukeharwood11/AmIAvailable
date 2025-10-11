from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

# Util models


class EventRequestApprovalUser(BaseModel):
    """Request model for creating an event request approval for a user"""

    user_id: str = Field(
        description="UUID of the user who needs to approve",
        examples=["user-123e4567-e89b-12d3-a456-426614174000"],
    )
    required: bool = Field(
        False, description="Whether this approval is required", examples=[True]
    )


# ============================================================================
# REQUEST MODELS
# ============================================================================


class CreateEventRequestApprovalRequest(BaseModel):
    """Request model for creating an event request approval"""

    event_request_id: str = Field(
        description="UUID of the event request",
        examples=["req-123e4567-e89b-12d3-a456-426614174000"],
    )
    user_id: str = Field(
        description="UUID of the user who needs to approve",
        examples=["user-123e4567-e89b-12d3-a456-426614174000"],
    )
    required: bool = Field(
        False, description="Whether this approval is required", examples=[True]
    )


class UpdateEventRequestApprovalRequest(BaseModel):
    """Request model for updating an event request approval"""

    approval_id: str = Field(
        description="UUID of the approval to update",
        examples=["approval-123e4567-e89b-12d3-a456-426614174000"],
    )
    status: Literal["pending", "approved", "rejected"] = Field(
        description="Approval status", examples=["approved"]
    )
    response_notes: str | None = Field(
        None,
        description="Optional notes from the approver",
        examples=["Looks good to me, approved!"],
    )


class GetEventRequestApprovalsRequest(BaseModel):
    """Request model for getting event request approvals"""

    event_request_id: str | None = Field(
        None,
        description="Filter by event request ID",
        examples=["req-123e4567-e89b-12d3-a456-426614174000"],
    )
    user_id: str | None = Field(
        None,
        description="Filter by user ID",
        examples=["user-123e4567-e89b-12d3-a456-426614174000"],
    )
    status: Literal["pending", "approved", "rejected"] | None = Field(
        None, description="Filter by approval status", examples=["pending"]
    )
    required: bool | None = Field(
        None, description="Filter by required approvals", examples=[True]
    )


class DeleteEventRequestApprovalRequest(BaseModel):
    """Request model for deleting an event request approval"""

    approval_id: str = Field(
        description="UUID of the approval to delete",
        examples=["approval-123e4567-e89b-12d3-a456-426614174000"],
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================


class EventRequestApprovalData(BaseModel):
    """Core event request approval data model"""

    id: str = Field(description="Approval UUID")
    event_request_id: str = Field(description="UUID of the event request")
    user_id: str = Field(description="UUID of the user who needs to approve")
    required: bool = Field(description="Whether this approval is required")
    status: str = Field(description="Approval status")
    response_notes: str | None = Field(description="Notes from the approver")
    responded_at: datetime | None = Field(description="When the user responded")
    created_at: datetime = Field(description="When the approval was created")
    updated_at: datetime = Field(description="When the approval was last updated")


class EventRequestApprovalResponse(BaseModel):
    """Response model for single event request approval operations"""

    status: str = "success"
    event_request_approval: EventRequestApprovalData
    message: str | None = None


class EventRequestApprovalsListResponse(BaseModel):
    """Response model for listing event request approvals"""

    status: str = "success"
    event_request_approvals: list[EventRequestApprovalData]
    count: int
    filters: dict[str, str | bool] | None = None


class EventRequestApprovalDeleteResponse(BaseModel):
    """Response model for event request approval deletion"""

    status: str = "success"
    message: str = "Event request approval deleted successfully"


class EventRequestApprovalCreateResponse(BaseModel):
    """Response model for event request approval creation"""

    status: str = "success"
    event_request_approval: EventRequestApprovalData
    message: str = "Event request approval created successfully"


class EventRequestApprovalsBatchCreateResponse(BaseModel):
    """Response model for batch event request approval creation"""

    status: str = "success"
    event_request_approvals: list[EventRequestApprovalData]
    count: int
    message: str = "Event request approvals created successfully"


class EventRequestApprovalUpdateResponse(BaseModel):
    """Response model for event request approval updates"""

    status: str = "success"
    event_request_approval: EventRequestApprovalData
    message: str = "Event request approval updated successfully"
