from fastapi import HTTPException
from api.databridge.relationship_requests_databridge import (
    RelationshipRequestsDatabridge,
    DBRelationshipRequestResponse,
    DBRelationshipRequestResponseWithUser,
)
from api.models.v1.relationship_requests import (
    RelationshipRequestData,
    RelationshipRequestCreateResponse,
    RelationshipRequestUpdateResponse,
    RelationshipRequestDeleteResponse,
    RelationshipRequestsListResponse,
    RelationshipRequestWithUserListResponse,
    RelationshipRequestResponse,
    RelationshipRequestWithUserData,
)
import api.models.v1.users as users
from api.services.relationships_service import RelationshipsService


class RelationshipRequestsService:
    def __init__(
        self,
        databridge: RelationshipRequestsDatabridge,
        relationships_service: RelationshipsService,
    ):
        self.databridge: RelationshipRequestsDatabridge = databridge
        self.relationships_service: RelationshipsService = relationships_service

    def _convert_db_to_model(
        self,
        db_request: (
            DBRelationshipRequestResponse | DBRelationshipRequestResponseWithUser
        ),
    ) -> RelationshipRequestData | RelationshipRequestWithUserData:
        """Convert database response to API model"""
        if isinstance(db_request, DBRelationshipRequestResponseWithUser):
            return RelationshipRequestWithUserData(
                id=db_request.id,
                requester=users.UserData(
                    id=db_request.requester.id,
                    full_name=db_request.requester.full_name,
                    email=db_request.requester.email,
                ),
                requested_email=db_request.requested_email,
                status=db_request.status,
                created_at=db_request.created_at,
                updated_at=db_request.updated_at,
            )
        else:
            return RelationshipRequestData(
                id=db_request.id,
                requester_id=db_request.requester_id,
                requested_email=db_request.requested_email,
                status=db_request.status,
                created_at=db_request.created_at,
                updated_at=db_request.updated_at,
            )

    async def create_relationship_request(
        self, *, requester_id: str, requester_email: str, requested_email: str
    ) -> RelationshipRequestCreateResponse:
        """Create a new relationship request via email"""
        # Check if request already exists
        if requester_email == requested_email:
            raise HTTPException(
                status_code=400,
                detail="Silly goose, you cannot send a relationship request to yourself",
            )

        existing = await self.databridge.check_existing_request(
            requester_id=requester_id, requested_email=requested_email
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="A relationship request already exists for this email",
            )

        # check to see if you're already connected to this user
        # TODO: implement this check

        # Create the relationship request
        db_request = await self.databridge.create_relationship_request(
            requester_id=requester_id, requested_email=requested_email
        )

        if not db_request:
            raise HTTPException(
                status_code=500, detail="Failed to create relationship request"
            )

        request_data = self._convert_db_to_model(db_request)
        return RelationshipRequestCreateResponse(relationship_request=request_data)

    async def get_relationship_request(
        self, *, request_id: str
    ) -> RelationshipRequestResponse:
        """Get a specific relationship request by ID"""
        db_request = await self.databridge.get_relationship_request_by_id(
            request_id=request_id
        )

        if not db_request:
            raise HTTPException(
                status_code=404, detail="Relationship request not found"
            )

        request_data = self._convert_db_to_model(db_request)
        return RelationshipRequestResponse(relationship_request=request_data)

    async def get_sent_relationship_requests(
        self, *, requester_id: str, status: str | None = None
    ) -> RelationshipRequestsListResponse:
        """Get all relationship requests sent by a user"""
        db_requests = await self.databridge.get_sent_relationship_requests(
            requester_id=requester_id, status=status
        )

        requests = [self._convert_db_to_model(req) for req in db_requests]

        filters: dict[str, str] = {"request_type": "sent"}
        if status:
            filters["status"] = status

        return RelationshipRequestsListResponse(
            relationship_requests=requests, count=len(requests), filters=filters
        )

    async def get_received_relationship_requests(
        self, *, user_email: str, status: str | None = None
    ) -> RelationshipRequestWithUserListResponse:
        """Get all relationship requests received by a user (by email)"""
        db_requests = await self.databridge.get_received_relationship_requests(
            user_email=user_email, status=status
        )

        requests = [self._convert_db_to_model(req) for req in db_requests]

        filters: dict[str, str] = {"request_type": "received"}
        if status:
            filters["status"] = status

        return RelationshipRequestWithUserListResponse(
            relationship_requests=requests, count=len(requests), filters=filters
        )

    async def update_relationship_request(
        self, *, request_id: str, user_id: str, user_email: str, status: str
    ) -> RelationshipRequestUpdateResponse:
        """Update a relationship request status"""
        # First verify the request exists
        existing = await self.databridge.get_relationship_request_by_id(
            request_id=request_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Relationship request not found"
            )

        # Check if user has permission to update this request
        # User can update if they are the requester or the requested user (by email)
        if existing.requester_id != user_id and existing.requested_email != user_email:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this relationship request",
            )

        # Update the request
        db_request = await self.databridge.update_relationship_request(
            request_id=request_id, status=status
        )

        if not db_request:
            raise HTTPException(
                status_code=500, detail="Failed to update relationship request"
            )

        request_data = self._convert_db_to_model(db_request)
        return RelationshipRequestUpdateResponse(relationship_request=request_data)

    async def delete_relationship_request(
        self, *, request_id: str, user_id: str, user_email: str
    ) -> RelationshipRequestDeleteResponse:
        """Delete a relationship request"""
        # First verify the request exists
        existing = await self.databridge.get_relationship_request_by_id(
            request_id=request_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Relationship request not found"
            )

        # Check if user has permission to delete this request
        # User can delete if they are the requester or the requested user (by email)
        if existing.requester_id != user_id and existing.requested_email != user_email:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this relationship request",
            )

        # Delete the request
        success = await self.databridge.delete_relationship_request(
            request_id=request_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete relationship request"
            )

        return RelationshipRequestDeleteResponse()

    async def approve_relationship_request(
        self, *, request_id: str, user_id: str, user_email: str
    ) -> RelationshipRequestUpdateResponse:
        """Approve a pending relationship request"""

        _update_response = await self.update_relationship_request(
            request_id=request_id,
            user_id=user_id,
            user_email=user_email,
            status="approved",
        )

        if not _update_response:
            raise HTTPException(
                status_code=500, detail="Failed to update relationship request"
            )

        # create a relationship
        _create_response = await self.relationships_service.create_relationship(
            user_id_1=_update_response.relationship_request.requester_id,
            user_id_2=user_id,
        )

        return _update_response

    async def reject_relationship_request(
        self, *, request_id: str, user_id: str, user_email: str
    ) -> RelationshipRequestUpdateResponse:
        """Reject a pending relationship request"""
        return await self.update_relationship_request(
            request_id=request_id,
            user_id=user_id,
            user_email=user_email,
            status="rejected",
        )
