from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any
import asyncio

from api.settings.auth import get_current_user_id, get_current_user
from api.dependencies import get_relationship_requests_service
from api.services.relationship_requests_service import RelationshipRequestsService
from api.models.v1.relationship_requests import (
    CreateRelationshipRequestRequest,
    RelationshipRequestWithUserListResponse,
    UpdateRelationshipRequestRequest,
    RelationshipRequestResponse,
    RelationshipRequestsListResponse,
    RelationshipRequestCreateResponse,
    RelationshipRequestUpdateResponse,
    RelationshipRequestDeleteResponse,
)
from api.services.notifications_service import (
    RelationshipNotificationPayload,
    User,
    NotificationsService,
)
from api.dependencies import get_notifications_service


router = APIRouter(prefix="/relationship-requests", tags=["Relationship Requests"])


@router.post("", response_model=RelationshipRequestCreateResponse)
async def create_relationship_request(
    request: CreateRelationshipRequestRequest,
    user: dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
    notification_service: NotificationsService = Depends(get_notifications_service),
) -> RelationshipRequestCreateResponse:
    """
    Create a new relationship request by email

    Returns:
        Created relationship request data
    """
    _relationship_request = await service.create_relationship_request(
        requester_id=user["user_id"],
        requester_email=str(user["email"]),
        requested_email=str(request.requested_email),
    )
    # TODO: Luke, you're dumb, either make the notifications able to be created from emails as well
    # or create the notifications when they create an account...
    #
    # _ = asyncio.create_task(
    #     notification_service.create_relationship_notification(
    #         to_user_id=request.requested_email,
    #         payload=RelationshipNotificationPayload(
    #             id=_relationship_request.relationship_request.id,
    #             update="created",
    #             user=User(id=user["user_id"], email=user["email"], name=user["user"].user_metadata.get("full_name"))
    #         )
    #     )
    # )
    return _relationship_request


@router.get("/sent", response_model=RelationshipRequestsListResponse)
async def get_sent_relationship_requests(
    status: str | None = Query(None, description="Filter by request status"),
    user_id: str = Depends(get_current_user_id),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestsListResponse:
    """
    Get all relationship requests sent by the current user

    Returns:
        List of sent relationship requests
    """
    return await service.get_sent_relationship_requests(
        requester_id=user_id, status=status
    )


@router.get("/received", response_model=RelationshipRequestWithUserListResponse)
async def get_received_relationship_requests(
    status: str | None = Query(None, description="Filter by request status"),
    user_data: Dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestWithUserListResponse:
    """
    Get all relationship requests received by the current user (by email)

    Returns:
        List of received relationship requests
    """
    user_email = user_data.get("email")
    if not user_email:
        raise HTTPException(status_code=400, detail="User email not found")

    return await service.get_received_relationship_requests(
        user_email=user_email, status=status
    )


@router.get("/{request_id}", response_model=RelationshipRequestResponse)
async def get_relationship_request(
    request_id: str,
    user_id: str = Depends(get_current_user_id),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestResponse:
    """
    Get a specific relationship request by ID

    Returns:
        Relationship request data
    """
    return await service.get_relationship_request(request_id=request_id)


@router.patch("/{request_id}", response_model=RelationshipRequestUpdateResponse)
async def update_relationship_request(
    request_id: str,
    request: UpdateRelationshipRequestRequest,
    user_data: Dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestUpdateResponse:
    """
    Update a relationship request status

    Returns:
        Updated relationship request data
    """
    user_id = user_data.get("user_id")
    user_email = user_data.get("email")

    if not user_id or not user_email:
        raise HTTPException(status_code=400, detail="User data not found")

    return await service.update_relationship_request(
        request_id=request_id,
        user_id=user_id,
        user_email=user_email,
        status=request.status,
    )


@router.delete("/{request_id}", response_model=RelationshipRequestDeleteResponse)
async def delete_relationship_request(
    request_id: str,
    user_data: Dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestDeleteResponse:
    """
    Delete a relationship request

    Returns:
        Deletion confirmation
    """
    user_id = user_data.get("user_id")
    user_email = user_data.get("email")

    if not user_id or not user_email:
        raise HTTPException(status_code=400, detail="User data not found")

    return await service.delete_relationship_request(
        request_id=request_id, user_id=user_id, user_email=user_email
    )


@router.post("/{request_id}/approve", response_model=RelationshipRequestUpdateResponse)
async def approve_relationship_request(
    request_id: str,
    user_data: Dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestUpdateResponse:
    """
    Approve a pending relationship request

    Returns:
        Updated relationship request data with approved status
    """
    user_id = user_data.get("user_id")
    user_email = user_data.get("email")

    if not user_id or not user_email:
        raise HTTPException(status_code=400, detail="User data not found")

    return await service.approve_relationship_request(
        request_id=request_id, user_id=user_id, user_email=user_email
    )


@router.post("/{request_id}/reject", response_model=RelationshipRequestUpdateResponse)
async def reject_relationship_request(
    request_id: str,
    user_data: Dict[str, Any] = Depends(get_current_user),
    service: RelationshipRequestsService = Depends(get_relationship_requests_service),
) -> RelationshipRequestUpdateResponse:
    """
    Reject a pending relationship request

    Returns:
        Updated relationship request data with rejected status
    """
    user_id = user_data.get("user_id")
    user_email = user_data.get("email")

    if not user_id or not user_email:
        raise HTTPException(status_code=400, detail="User data not found")

    return await service.reject_relationship_request(
        request_id=request_id, user_id=user_id, user_email=user_email
    )
