from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DBUserData(BaseModel):
    id: str
    email: str
    full_name: str


class DBRelationshipRequestResponse(BaseModel):
    id: str
    requester_id: str
    requested_email: str
    status: str
    created_at: datetime
    updated_at: datetime


class DBRelationshipRequestResponseWithUser(BaseModel):
    id: str
    requested_email: str
    status: str
    created_at: datetime
    updated_at: datetime
    requester: DBUserData


class RelationshipRequestsDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.relationship_requests = self.supabase.table("relationship_requests")

    async def create_relationship_request(
        self, *, requester_id: str, requested_email: str
    ) -> DBRelationshipRequestResponse | None:
        """Create a new relationship request"""
        try:
            data = {
                "requester_id": requester_id,
                "requested_email": requested_email,
                "status": "pending",
            }

            response = self.relationship_requests.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBRelationshipRequestResponse(**_data)
        except Exception as e:
            logger.info(f"Error creating relationship request: {e}")
            return None

    async def get_relationship_request_by_id(
        self, *, request_id: str
    ) -> DBRelationshipRequestResponse | None:
        """Get a specific relationship request by ID"""
        try:
            response = self.supabase.rpc(
                "get_relationship_request_with_user", {"p_request_id": request_id}
            ).execute()

            if not response.data or len(response.data) == 0:
                return None

            row = response.data[0]

            # Create the user data
            user_data = DBUserData(
                id=row["user_id"],
                email=row["user_email"],
                full_name=row["user_full_name"],
            )

            # Create the relationship request data
            return DBRelationshipRequestResponse(
                id=row["id"],
                requester_id=row["requester_id"],
                requested_email=row["requested_email"],
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                requester=user_data,
            )
        except Exception as e:
            logger.info(f"Error fetching relationship request: {e}")
            return None

    async def get_sent_relationship_requests(
        self, *, requester_id: str, status: str | None = None
    ) -> list[DBRelationshipRequestResponse]:
        """Get all relationship requests sent by a user"""
        try:
            response = self.supabase.rpc(
                "get_sent_relationship_requests",
                {"p_requester_id": requester_id, "p_status": status},
            ).execute()

            if not response.data:
                return []

            result = []
            for row in response.data:
                # Create the user data
                user_data = DBUserData(
                    id=row["user_id"],
                    email=row["user_email"],
                    full_name=row["user_full_name"],
                )

                # Create the relationship request data
                request_data = DBRelationshipRequestResponse(
                    id=row["id"],
                    requester_id=row["requester_id"],
                    requested_email=row["requested_email"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    requester=user_data,
                )
                result.append(request_data)

            return result
        except Exception as e:
            logger.info(f"Error fetching sent relationship requests: {e}")
            return []

    async def get_received_relationship_requests(
        self, *, user_email: str, status: str | None = None
    ) -> list[DBRelationshipRequestResponseWithUser]:
        """Get all relationship requests received by a user (by email)"""
        try:
            response = self.supabase.rpc(
                "get_received_relationship_requests",
                {"p_requested_email": user_email, "p_status": status},
            ).execute()

            if not response.data:
                return []

            result = []
            for row in response.data:
                # Create the user data
                user_data = DBUserData(
                    id=row["user_id"],
                    email=row["user_email"],
                    full_name=row["user_full_name"],
                )

                # Create the relationship request data
                request_data = DBRelationshipRequestResponseWithUser(
                    id=row["id"],
                    requested_email=row["requested_email"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    requester=user_data,
                )
                result.append(request_data)

            return result
        except Exception as e:
            logger.info(f"Error fetching received relationship requests: {e}")
            return []

    async def update_relationship_request(
        self, *, request_id: str, status: str
    ) -> DBRelationshipRequestResponse | None:
        """Update a relationship request status"""
        try:
            # First update the record
            update_data = {"status": status, "updated_at": datetime.now().isoformat()}

            response = (
                self.relationship_requests.update(update_data)
                .eq("id", request_id)
                .execute()
            )
            if not response.data:
                return None

            # Then fetch the updated record with user data
            return await self.get_relationship_request_by_id(request_id=request_id)
        except Exception as e:
            logger.info(f"Error updating relationship request: {e}")
            return None

    async def delete_relationship_request(self, *, request_id: str) -> bool:
        """Delete a relationship request"""
        try:
            response = (
                self.relationship_requests.delete().eq("id", request_id).execute()
            )
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            logger.info(f"Error deleting relationship request: {e}")
            return False

    async def check_existing_request(
        self, *, requester_id: str, requested_email: str
    ) -> DBRelationshipRequestResponse | None:
        """Check if a relationship request already exists"""
        try:
            response = (
                self.relationship_requests.select("*")
                .eq("requester_id", requester_id)
                .eq("requested_email", requested_email)
                .execute()
            )

            if not response.data:
                return None

            return DBRelationshipRequestResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error checking existing request: {e}")
            return None
