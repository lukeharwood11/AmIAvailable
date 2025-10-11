from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class DBEventRequestResponse(BaseModel):
    id: str
    google_event_id: str | None
    title: str | None
    location: str | None
    description: str | None
    start_date: dict  # JSONB field
    end_date: dict  # JSONB field
    importance_level: int
    status: str
    notes: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime


class DBEventRequestWithApprovalsResponse(BaseModel):
    id: str
    google_event_id: str | None
    title: str | None
    location: str | None
    description: str | None
    start_date: dict  # JSONB field
    end_date: dict  # JSONB field
    importance_level: int
    status: str
    notes: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime
    approval_status: str
    requested_approvals: int
    completed_count: int
    total_count: int


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


class DBEventRequestWithApproversResponse(BaseModel):
    id: str
    google_event_id: str | None
    title: str | None
    location: str | None
    description: str | None
    start_date: dict  # JSONB field
    end_date: dict  # JSONB field
    importance_level: int
    status: str
    notes: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime
    approvers: list[DBEventRequestApprovalResponse]


class EventRequestsDatabridge:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.event_requests = self.supabase.table("event_requests")

    async def create_event_request(
        self,
        *,
        google_event_id: str | None,
        title: str | None,
        location: str | None,
        description: str | None,
        start_date: dict,
        end_date: dict,
        importance_level: int,
        notes: str | None,
        created_by: str,
    ) -> DBEventRequestResponse | None:
        """Create a new event request"""
        try:
            data = {
                "google_event_id": google_event_id,
                "title": title,
                "location": location,
                "description": description,
                "start_date": start_date,
                "end_date": end_date,
                "importance_level": importance_level,
                "status": "pending",
                "notes": notes,
                "created_by": created_by,
            }

            response = self.event_requests.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBEventRequestResponse(**_data)
        except Exception as e:
            logger.info(f"Error creating event request: {e}")
            return None

    async def get_event_request_by_id(
        self, *, event_request_id: str
    ) -> DBEventRequestResponse | None:
        """Get a specific event request by ID"""
        try:
            response = (
                self.event_requests.select("*")
                .eq("id", event_request_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBEventRequestResponse(**response.data)
        except Exception as e:
            logger.info(f"Error fetching event request: {e}")
            return None

    async def get_user_event_requests(
        self,
        *,
        user_id: str,
        status: str | None = None,
        importance_level: int | None = None,
        start_date_from: dict | None = None,
        start_date_to: dict | None = None,
    ) -> list[DBEventRequestResponse]:
        """Get all event requests created by a user with optional filters"""
        try:
            query = self.event_requests.select("*").eq("created_by", user_id)

            if status:
                query = query.eq("status", status)
            if importance_level:
                query = query.eq("importance_level", importance_level)
            # Note: Date filtering on JSONB fields would require more complex queries
            # For now, we'll filter in the application layer if needed

            response = query.order("created_at", desc=True).execute()
            if not response.data:
                return []

            return [DBEventRequestResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error fetching user event requests: {e}")
            return []

    async def get_all_event_requests(
        self,
        *,
        status: str | None = None,
        importance_level: int | None = None,
        start_date_from: dict | None = None,
        start_date_to: dict | None = None,
        created_by: str | None = None,
    ) -> list[DBEventRequestResponse]:
        """Get all event requests with optional filters"""
        try:
            query = self.event_requests.select("*")

            if status:
                query = query.eq("status", status)
            if importance_level:
                query = query.eq("importance_level", importance_level)
            if created_by:
                query = query.eq("created_by", created_by)
            # Note: Date filtering on JSONB fields would require more complex queries
            # For now, we'll filter in the application layer if needed

            response = query.order("created_at", desc=True).execute()
            if not response.data:
                return []

            return [DBEventRequestResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error fetching all event requests: {e}")
            return []

    async def update_event_request(
        self,
        *,
        event_request_id: str,
        google_event_id: str | None = None,
        title: str | None = None,
        location: str | None = None,
        description: str | None = None,
        start_date: dict | None = None,
        end_date: dict | None = None,
        importance_level: int | None = None,
        status: str | None = None,
        notes: str | None = None,
    ) -> DBEventRequestResponse | None:
        """Update an event request"""
        try:
            update_data: dict[str, str | int | dict] = {
                "updated_at": datetime.now().isoformat()
            }

            if google_event_id is not None:
                update_data["google_event_id"] = google_event_id
            if title is not None:
                update_data["title"] = title
            if location is not None:
                update_data["location"] = location
            if description is not None:
                update_data["description"] = description
            if start_date is not None:
                update_data["start_date"] = start_date
            if end_date is not None:
                update_data["end_date"] = end_date
            if importance_level is not None:
                update_data["importance_level"] = importance_level
            if status is not None:
                update_data["status"] = status
            if notes is not None:
                update_data["notes"] = notes

            response = (
                self.event_requests.update(update_data)
                .eq("id", event_request_id)
                .execute()
            )
            if not response.data:
                return None

            return DBEventRequestResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error updating event request: {e}")
            return None

    async def delete_event_request(self, *, event_request_id: str) -> bool:
        """Delete an event request"""
        try:
            response = self.event_requests.delete().eq("id", event_request_id).execute()
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            logger.info(f"Error deleting event request: {e}")
            return False

    async def get_event_request_by_google_id(
        self, *, google_event_id: str
    ) -> DBEventRequestResponse | None:
        """Get an event request by Google Calendar event ID"""
        try:
            response = (
                self.event_requests.select("*")
                .eq("google_event_id", google_event_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBEventRequestResponse(**response.data)
        except Exception as e:
            logger.info(f"Error fetching event request by Google ID: {e}")
            return None

    async def list_event_requests_with_approvals(
        self,
        *,
        user_id: str | None = None,
        status: str | None = None,
        skip: int = 0,
        take: int = 50,
    ) -> list[DBEventRequestWithApprovalsResponse]:
        """List event requests with approval status aggregation using SQL function"""
        try:
            response = self.supabase.rpc(
                "list_event_requests_with_approvals",
                {
                    "p_user_id": user_id,
                    "p_status": status,
                    "p_skip": skip,
                    "p_take": take,
                },
            ).execute()

            if not response.data:
                return []

            return [
                DBEventRequestWithApprovalsResponse(**item) for item in response.data
            ]
        except Exception as e:
            logger.info(f"Error listing event requests with approvals: {e}")
            return []

    async def get_event_request_with_approvers(
        self, *, event_request_id: str
    ) -> DBEventRequestWithApproversResponse | None:
        """Get a specific event request with all its approvers and approval data"""
        try:
            # Get the event request
            event_response = (
                self.event_requests.select("*")
                .eq("id", event_request_id)
                .single()
                .execute()
            )

            if not event_response.data:
                return None

            # Get all approvals for this event request
            approvals_response = (
                self.supabase.table("event_request_approvals")
                .select("*")
                .eq("event_request_id", event_request_id)
                .execute()
            )

            approvers = []
            if approvals_response.data:
                approvers = [
                    DBEventRequestApprovalResponse(**approval)
                    for approval in approvals_response.data
                ]

            # Combine event request with approvers
            event_data = event_response.data
            event_data["approvers"] = approvers

            return DBEventRequestWithApproversResponse(**event_data)
        except Exception as e:
            logger.info(f"Error fetching event request with approvers: {e}")
            return None
