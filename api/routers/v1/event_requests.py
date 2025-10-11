from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from ...settings.auth import get_current_user_id, get_current_user
from ...models.v1.event_requests import EventDateTime
from ...dependencies import (
    get_event_requests_service,
    get_event_request_approvals_service,
)
from ...services.event_requests_service import EventRequestsService
from ...services.event_request_approvals_service import EventRequestApprovalsService
from ...models.v1.event_requests import (
    CreateEventRequestRequest,
    SmartParseEventRequestRequest,
    UpdateEventRequestRequest,
    EventRequestResponse,
    EventRequestWithApproversResponse,
    EventRequestsListResponse,
    EventRequestsWithApprovalsListResponse,
    EventRequestCreateResponse,
    EventRequestUpdateResponse,
    EventRequestDeleteResponse,
    SmartParseEventRequestResponse,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/event-requests", tags=["Event Requests"])


@router.post("/commands/auto-fill")
async def auto_fill_event_request(
    request: SmartParseEventRequestRequest,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> SmartParseEventRequestResponse:
    """
    Auto-fill an event request by description
    """
    _parsed = await service.auto_fill_event_request(
        request=request,
        user_id=user_id,
    )
    return SmartParseEventRequestResponse(event_request=_parsed)


@router.post("", response_model=EventRequestCreateResponse)
async def create_event_request(
    request: CreateEventRequestRequest,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
    event_request_approvals_service: EventRequestApprovalsService = Depends(
        get_event_request_approvals_service
    ),
) -> EventRequestCreateResponse:
    """
    Create a new event request

    Returns:
        Created event request data
    """
    _event_request = await service.create_event_request(
        google_event_id=request.google_event_id,
        title=request.title,
        location=request.location,
        description=request.description,
        start_date=request.start_date,
        end_date=request.end_date,
        importance_level=request.importance_level,
        notes=request.notes,
        created_by=user_id,
    )
    try:
        if request.approvers:
            _approvers = await event_request_approvals_service.create_event_request_approvals_batch(
                event_request_id=_event_request.event_request.id,
                approvals_request=request.approvers,
            )
    except Exception as e:
        # rollback the event request
        await service.delete_event_request(
            event_request_id=_event_request.event_request.id,
            user_id=user_id,
        )
        logger.error(f"Error creating event request approvals: {e}")
    return _event_request


@router.get("", response_model=EventRequestsListResponse)
async def get_user_event_requests(
    status: str | None = Query(None, description="Filter by event request status"),
    importance_level: int | None = Query(
        None, ge=1, le=5, description="Filter by importance level"
    ),
    start_date_from: datetime | None = Query(
        None, description="Filter events starting from this date"
    ),
    start_date_to: datetime | None = Query(
        None, description="Filter events starting before this date"
    ),
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestsListResponse:
    """
    Get all event requests created by the current user with optional filters

    Returns:
        List of user's event requests
    """
    # Convert datetime to EventDateTime
    start_date_from_event = None
    if start_date_from:
        start_date_from_event = EventDateTime(date_time=start_date_from)

    start_date_to_event = None
    if start_date_to:
        start_date_to_event = EventDateTime(date_time=start_date_to)

    return await service.get_user_event_requests(
        user_id=user_id,
        status=status,
        importance_level=importance_level,
        start_date_from=start_date_from_event,
        start_date_to=start_date_to_event,
    )


@router.get("/all", response_model=EventRequestsListResponse)
async def get_all_event_requests(
    status: str | None = Query(None, description="Filter by event request status"),
    importance_level: int | None = Query(
        None, ge=1, le=5, description="Filter by importance level"
    ),
    start_date_from: datetime | None = Query(
        None, description="Filter events starting from this date"
    ),
    start_date_to: datetime | None = Query(
        None, description="Filter events starting before this date"
    ),
    created_by: str | None = Query(None, description="Filter by creator user ID"),
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestsListResponse:
    """
    Get all event requests with optional filters (potentially for admin/system use)

    Returns:
        List of event requests
    """
    # Convert datetime to EventDateTime
    start_date_from_event = None
    if start_date_from:
        start_date_from_event = EventDateTime(date_time=start_date_from)

    start_date_to_event = None
    if start_date_to:
        start_date_to_event = EventDateTime(date_time=start_date_to)

    return await service.get_all_event_requests(
        status=status,
        importance_level=importance_level,
        start_date_from=start_date_from_event,
        start_date_to=start_date_to_event,
        created_by=created_by,
    )


@router.get("/with-approvals", response_model=EventRequestsWithApprovalsListResponse)
async def list_event_requests_with_approvals(
    status: str | None = Query(None, description="Filter by event request status"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    take: int = Query(
        50, ge=1, le=100, description="Number of records to return (max 100)"
    ),
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestsWithApprovalsListResponse:
    """
    List event requests with approval status aggregation

    Returns event requests with:
    - approval_status: 'pending' if any are pending and none are rejected,
      'rejected' if any are rejected, 'approved' if all are approved,
      'no_approvals' if no approval requests exist
    - requested_approvals: total number of approval requests
    - completed_count: number of completed (non-pending) approvals
    - Pagination support with skip/take and total_count

    Returns:
        List of event requests with approval status information
    """
    return await service.list_event_requests_with_approvals(
        user_id=user_id,
        status=status,
        skip=skip,
        take=take,
    )


@router.get("/{event_request_id}", response_model=EventRequestResponse)
async def get_event_request(
    event_request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestResponse:
    """
    Get a specific event request by ID

    Returns:
        Event request data
    """
    return await service.get_event_request(event_request_id=event_request_id)


@router.get(
    "/{event_request_id}/with-approvers",
    response_model=EventRequestWithApproversResponse,
)
async def get_event_request_with_approvers(
    event_request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestWithApproversResponse:
    """
    Get a specific event request with all its approvers and approval data

    Returns:
        Event request data with detailed approvers information including:
        - All approvers assigned to this event request
        - Approval status for each approver (pending, approved, rejected)
        - Response notes from approvers
        - Timestamps for when approvals were created and responded to
    """
    return await service.get_event_request_with_approvers(
        event_request_id=event_request_id
    )


@router.get("/google/{google_event_id}", response_model=EventRequestResponse)
async def get_event_request_by_google_id(
    google_event_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestResponse:
    """
    Get an event request by Google Calendar event ID

    Returns:
        Event request data
    """
    return await service.get_event_request_by_google_id(google_event_id=google_event_id)


@router.patch("/{event_request_id}", response_model=EventRequestUpdateResponse)
async def update_event_request(
    event_request_id: str,
    request: UpdateEventRequestRequest,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestUpdateResponse:
    """
    Update an event request

    Returns:
        Updated event request data
    """
    return await service.update_event_request(
        event_request_id=event_request_id,
        user_id=user_id,
        google_event_id=request.google_event_id,
        title=request.title,
        location=request.location,
        description=request.description,
        start_date=request.start_date,
        end_date=request.end_date,
        importance_level=request.importance_level,
        status=request.status,
        notes=request.notes,
    )


@router.delete("/{event_request_id}", response_model=EventRequestDeleteResponse)
async def delete_event_request(
    event_request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestDeleteResponse:
    """
    Delete an event request

    Returns:
        Deletion confirmation
    """
    return await service.delete_event_request(
        event_request_id=event_request_id, user_id=user_id
    )


@router.post("/{event_request_id}/approve", response_model=EventRequestUpdateResponse)
async def approve_event_request(
    event_request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestUpdateResponse:
    """
    Approve a pending event request

    Returns:
        Updated event request data with approved status
    """
    return await service.approve_event_request(
        event_request_id=event_request_id, user_id=user_id
    )


@router.post("/{event_request_id}/reject", response_model=EventRequestUpdateResponse)
async def reject_event_request(
    event_request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: EventRequestsService = Depends(get_event_requests_service),
) -> EventRequestUpdateResponse:
    """
    Reject a pending event request

    Returns:
        Updated event request data with rejected status
    """
    return await service.reject_event_request(
        event_request_id=event_request_id, user_id=user_id
    )
