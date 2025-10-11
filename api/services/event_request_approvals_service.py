from fastapi import HTTPException
from api.databridge.event_request_approvals_databridge import (
    EventRequestApprovalsDatabridge,
    DBEventRequestApprovalResponse,
)
from api.models.v1.event_request_approvals import (
    EventRequestApprovalData,
    EventRequestApprovalCreateResponse,
    EventRequestApprovalsBatchCreateResponse,
    EventRequestApprovalUpdateResponse,
    EventRequestApprovalDeleteResponse,
    EventRequestApprovalsListResponse,
    EventRequestApprovalResponse,
)
import api.models.v1.event_request_approvals as era_models


class EventRequestApprovalsService:
    def __init__(self, databridge: EventRequestApprovalsDatabridge) -> None:
        self.databridge: EventRequestApprovalsDatabridge = databridge

    def _convert_db_to_model(
        self, db_approval: DBEventRequestApprovalResponse
    ) -> EventRequestApprovalData:
        """Convert database response to API model"""
        return EventRequestApprovalData(
            id=db_approval.id,
            event_request_id=db_approval.event_request_id,
            user_id=db_approval.user_id,
            required=db_approval.required,
            status=db_approval.status,
            response_notes=db_approval.response_notes,
            responded_at=db_approval.responded_at,
            created_at=db_approval.created_at,
            updated_at=db_approval.updated_at,
        )

    async def create_event_request_approvals_batch(
        self,
        *,
        event_request_id: str,
        approvals_request: list[era_models.EventRequestApprovalUser],
    ) -> EventRequestApprovalsBatchCreateResponse:
        """Create a batch of event request approvals"""
        db_approvals = await self.databridge.create_event_request_approvals_batch(
            event_request_id=event_request_id, approvals_request=approvals_request
        )

        # Convert database responses to API models
        approval_data_list = [
            self._convert_db_to_model(approval) for approval in db_approvals
        ]

        return EventRequestApprovalsBatchCreateResponse(
            event_request_approvals=approval_data_list, count=len(approval_data_list)
        )

    async def create_event_request_approval(
        self, *, event_request_id: str, user_id: str, required: bool = False
    ) -> EventRequestApprovalCreateResponse:
        """Create a new event request approval"""
        # Check if approval already exists for this user and event request
        existing = await self.databridge.check_existing_approval(
            event_request_id=event_request_id, user_id=user_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Approval already exists for this user and event request",
            )

        # Create the approval
        db_approval = await self.databridge.create_event_request_approval(
            event_request_id=event_request_id, user_id=user_id, required=required
        )

        if not db_approval:
            raise HTTPException(
                status_code=500, detail="Failed to create event request approval"
            )

        approval_data = self._convert_db_to_model(db_approval)
        return EventRequestApprovalCreateResponse(event_request_approval=approval_data)

    async def get_event_request_approval(
        self, *, approval_id: str
    ) -> EventRequestApprovalResponse:
        """Get a specific event request approval by ID"""
        db_approval = await self.databridge.get_event_request_approval_by_id(
            approval_id=approval_id
        )

        if not db_approval:
            raise HTTPException(
                status_code=404, detail="Event request approval not found"
            )

        approval_data = self._convert_db_to_model(db_approval)
        return EventRequestApprovalResponse(event_request_approval=approval_data)

    async def get_event_request_approvals(
        self,
        *,
        event_request_id: str | None = None,
        user_id: str | None = None,
        status: str | None = None,
        required: bool | None = None,
    ) -> EventRequestApprovalsListResponse:
        """Get event request approvals with optional filters"""
        db_approvals = await self.databridge.get_event_request_approvals(
            event_request_id=event_request_id,
            user_id=user_id,
            status=status,
            required=required,
        )

        approvals = [self._convert_db_to_model(approval) for approval in db_approvals]

        filters: dict[str, str | bool] = {}
        if event_request_id:
            filters["event_request_id"] = event_request_id
        if user_id:
            filters["user_id"] = user_id
        if status:
            filters["status"] = status
        if required is not None:
            filters["required"] = required

        return EventRequestApprovalsListResponse(
            event_request_approvals=approvals,
            count=len(approvals),
            filters=filters if filters else None,
        )

    async def get_approvals_by_event_request(
        self, *, event_request_id: str
    ) -> EventRequestApprovalsListResponse:
        """Get all approvals for a specific event request"""
        db_approvals = await self.databridge.get_approvals_by_event_request(
            event_request_id=event_request_id
        )

        approvals = [self._convert_db_to_model(approval) for approval in db_approvals]

        return EventRequestApprovalsListResponse(
            event_request_approvals=approvals,
            count=len(approvals),
            filters={"event_request_id": event_request_id},
        )

    async def get_user_pending_approvals(
        self, *, user_id: str
    ) -> EventRequestApprovalsListResponse:
        """Get all pending approvals for a user"""
        db_approvals = await self.databridge.get_user_pending_approvals(user_id=user_id)

        approvals = [self._convert_db_to_model(approval) for approval in db_approvals]

        return EventRequestApprovalsListResponse(
            event_request_approvals=approvals,
            count=len(approvals),
            filters={"user_id": user_id, "status": "pending"},
        )

    async def update_event_request_approval(
        self,
        *,
        approval_id: str,
        user_id: str,
        status: str,
        response_notes: str | None = None,
    ) -> EventRequestApprovalUpdateResponse:
        """Update an event request approval (respond to it)"""
        # First verify the approval exists and user has permission
        existing = await self.databridge.get_event_request_approval_by_id(
            approval_id=approval_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Event request approval not found"
            )

        # Check if user is the one who needs to approve
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this approval",
            )

        # Update the approval
        db_approval = await self.databridge.update_event_request_approval(
            approval_id=approval_id, status=status, response_notes=response_notes
        )

        if not db_approval:
            raise HTTPException(
                status_code=500, detail="Failed to update event request approval"
            )

        approval_data = self._convert_db_to_model(db_approval)
        return EventRequestApprovalUpdateResponse(event_request_approval=approval_data)

    async def delete_event_request_approval(
        self, *, approval_id: str, user_id: str
    ) -> EventRequestApprovalDeleteResponse:
        """Delete an event request approval"""
        # First verify the approval exists and user has permission
        existing = await self.databridge.get_event_request_approval_by_id(
            approval_id=approval_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Event request approval not found"
            )

        # Check if user is the one who created the approval or the one who needs to approve
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this approval",
            )

        # Delete the approval
        success = await self.databridge.delete_event_request_approval(
            approval_id=approval_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete event request approval"
            )

        return EventRequestApprovalDeleteResponse()

    async def delete_approvals_by_event_request(
        self, *, event_request_id: str
    ) -> EventRequestApprovalDeleteResponse:
        """Delete all approvals for a specific event request (used when deleting event request)"""
        success = await self.databridge.delete_approvals_by_event_request(
            event_request_id=event_request_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete event request approvals"
            )

        return EventRequestApprovalDeleteResponse()

    async def check_all_required_approvals_complete(
        self, *, event_request_id: str
    ) -> bool:
        """Check if all required approvals for an event request are complete"""
        return await self.databridge.check_all_required_approvals_complete(
            event_request_id=event_request_id
        )

    async def approve_event_request(
        self, *, approval_id: str, user_id: str, response_notes: str | None = None
    ) -> EventRequestApprovalUpdateResponse:
        """Approve an event request"""
        return await self.update_event_request_approval(
            approval_id=approval_id,
            user_id=user_id,
            status="approved",
            response_notes=response_notes,
        )

    async def reject_event_request(
        self, *, approval_id: str, user_id: str, response_notes: str | None = None
    ) -> EventRequestApprovalUpdateResponse:
        """Reject an event request"""
        return await self.update_event_request_approval(
            approval_id=approval_id,
            user_id=user_id,
            status="rejected",
            response_notes=response_notes,
        )
