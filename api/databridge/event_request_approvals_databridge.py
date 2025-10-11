from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import api.models.v1.event_request_approvals as era_models


class DBEventRequestApprovalResponse(BaseModel):
    id: str
    event_request_id: str
    user_id: str
    required: bool
    status: str
    response_notes: str | None
    responded_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EventRequestApprovalsDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.event_request_approvals = self.supabase.table("event_request_approvals")

    async def create_event_request_approvals_batch(
        self,
        *,
        event_request_id: str,
        approvals_request: list[era_models.EventRequestApprovalUser],
    ) -> list[DBEventRequestApprovalResponse]:
        """Create a batch of event request approvals"""
        try:
            # Add event_request_id and status to each approval record
            data = []
            for approval in approvals_request:
                approval_data = approval.model_dump()
                approval_data["event_request_id"] = event_request_id
                approval_data["status"] = "pending"
                data.append(approval_data)

            response = self.event_request_approvals.insert(data).execute()
            if not response.data:
                return []
            return [DBEventRequestApprovalResponse(**item) for item in response.data]
        except Exception as e:
            print(f"Error creating event request approvals batch: {e}")
            return []

    async def create_event_request_approval(
        self, *, event_request_id: str, user_id: str, required: bool = False
    ) -> DBEventRequestApprovalResponse | None:
        """Create a new event request approval"""
        try:
            data = {
                "event_request_id": event_request_id,
                "user_id": user_id,
                "required": required,
                "status": "pending",
            }

            response = self.event_request_approvals.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBEventRequestApprovalResponse(**_data)
        except Exception as e:
            print(f"Error creating event request approval: {e}")
            return None

    async def get_event_request_approval_by_id(
        self, *, approval_id: str
    ) -> DBEventRequestApprovalResponse | None:
        """Get a specific event request approval by ID"""
        try:
            response = (
                self.event_request_approvals.select("*")
                .eq("id", approval_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBEventRequestApprovalResponse(**response.data)
        except Exception as e:
            print(f"Error fetching event request approval: {e}")
            return None

    async def get_event_request_approvals(
        self,
        *,
        event_request_id: str | None = None,
        user_id: str | None = None,
        status: str | None = None,
        required: bool | None = None,
    ) -> list[DBEventRequestApprovalResponse]:
        """Get event request approvals with optional filters"""
        try:
            query = self.event_request_approvals.select("*")

            if event_request_id:
                query = query.eq("event_request_id", event_request_id)
            if user_id:
                query = query.eq("user_id", user_id)
            if status:
                query = query.eq("status", status)
            if required is not None:
                query = query.eq("required", required)

            response = query.execute()
            if not response.data:
                return []

            return [DBEventRequestApprovalResponse(**item) for item in response.data]
        except Exception as e:
            print(f"Error fetching event request approvals: {e}")
            return []

    async def get_approvals_by_event_request(
        self, *, event_request_id: str
    ) -> list[DBEventRequestApprovalResponse]:
        """Get all approvals for a specific event request"""
        try:
            response = (
                self.event_request_approvals.select("*")
                .eq("event_request_id", event_request_id)
                .execute()
            )
            if not response.data:
                return []

            return [DBEventRequestApprovalResponse(**item) for item in response.data]
        except Exception as e:
            print(f"Error fetching approvals by event request: {e}")
            return []

    async def get_user_pending_approvals(
        self, *, user_id: str
    ) -> list[DBEventRequestApprovalResponse]:
        """Get all pending approvals for a user"""
        try:
            response = (
                self.event_request_approvals.select("*")
                .eq("user_id", user_id)
                .eq("status", "pending")
                .execute()
            )
            if not response.data:
                return []

            return [DBEventRequestApprovalResponse(**item) for item in response.data]
        except Exception as e:
            print(f"Error fetching user pending approvals: {e}")
            return []

    async def update_event_request_approval(
        self, *, approval_id: str, status: str, response_notes: str | None = None
    ) -> DBEventRequestApprovalResponse | None:
        """Update an event request approval"""
        try:
            update_data = {"status": status, "updated_at": datetime.now().isoformat()}

            if response_notes is not None:
                update_data["response_notes"] = response_notes

            # Set responded_at when status changes from pending
            if status != "pending":
                update_data["responded_at"] = datetime.now().isoformat()

            response = (
                self.event_request_approvals.update(update_data)
                .eq("id", approval_id)
                .execute()
            )
            if not response.data:
                return None

            return DBEventRequestApprovalResponse(**response.data[0])
        except Exception as e:
            print(f"Error updating event request approval: {e}")
            return None

    async def delete_event_request_approval(self, *, approval_id: str) -> bool:
        """Delete an event request approval"""
        try:
            response = (
                self.event_request_approvals.delete().eq("id", approval_id).execute()
            )
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            print(f"Error deleting event request approval: {e}")
            return False

    async def delete_approvals_by_event_request(self, *, event_request_id: str) -> bool:
        """Delete all approvals for a specific event request"""
        try:
            response = (
                self.event_request_approvals.delete()
                .eq("event_request_id", event_request_id)
                .execute()
            )
            return response.data is not None
        except Exception as e:
            print(f"Error deleting approvals by event request: {e}")
            return False

    async def check_existing_approval(
        self, *, event_request_id: str, user_id: str
    ) -> DBEventRequestApprovalResponse | None:
        """Check if an approval already exists for user and event request"""
        try:
            response = (
                self.event_request_approvals.select("*")
                .eq("event_request_id", event_request_id)
                .eq("user_id", user_id)
                .execute()
            )

            if not response.data:
                return None

            return DBEventRequestApprovalResponse(**response.data[0])
        except Exception as e:
            print(f"Error checking existing approval: {e}")
            return None

    async def check_all_required_approvals_complete(
        self, *, event_request_id: str
    ) -> bool:
        """Check if all required approvals for an event request are complete"""
        try:
            # Get all required approvals for this event request
            response = (
                self.event_request_approvals.select("*")
                .eq("event_request_id", event_request_id)
                .eq("required", True)
                .execute()
            )

            if not response.data:
                # No required approvals, so considered complete
                return True

            # Check if all required approvals are approved
            for approval in response.data:
                if approval["status"] != "approved":
                    return False

            return True
        except Exception as e:
            print(f"Error checking required approvals: {e}")
            return False
