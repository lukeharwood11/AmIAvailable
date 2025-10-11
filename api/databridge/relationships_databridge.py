from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DBRelationshipResponse(BaseModel):
    id: str
    user_id_1: str
    user_id_2: str
    created_at: datetime
    updated_at: datetime


class DBRelationshipWithUserResponse(BaseModel):
    id: str
    user_id_1: str
    user_id_2: str
    created_at: datetime
    updated_at: datetime
    other_user_id: str
    other_user_email: str
    other_user_full_name: str


class DBRelationshipsListResponse(BaseModel):
    relationships: list[DBRelationshipWithUserResponse]
    total_count: int


class RelationshipsDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.relationships = self.supabase.table("relationships")

    async def search_relationships(
        self, *, query: str, user_id: str
    ) -> list[DBRelationshipWithUserResponse]:
        """Search for relationships by query"""
        try:
            response = self.supabase.rpc(
                "search_relationships", {"p_query": query, "p_user_id": user_id}
            ).execute()
            if not response.data:
                return []
            return [DBRelationshipWithUserResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error searching relationships: {e}")
            return []

    async def create_relationship(
        self, *, user_id_1: str, user_id_2: str
    ) -> DBRelationshipResponse | None:
        """Create a new relationship between two users"""
        try:
            data = {"user_id_1": user_id_1, "user_id_2": user_id_2}

            response = self.relationships.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBRelationshipResponse(**_data)
        except Exception as e:
            logger.info(f"Error creating relationship: {e}")
            return None

    async def get_relationship_by_id(
        self, *, relationship_id: str
    ) -> DBRelationshipResponse | None:
        """Get a specific relationship by ID (legacy method for backward compatibility)"""
        try:
            response = (
                self.relationships.select("*")
                .eq("id", relationship_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBRelationshipResponse(**response.data)
        except Exception as e:
            logger.info(f"Error fetching relationship: {e}")
            return None

    async def get_relationship_by_id_with_user(
        self, *, relationship_id: str, current_user_id: str
    ) -> DBRelationshipWithUserResponse | None:
        """Get a specific relationship by ID with other user data"""
        try:
            response = self.supabase.rpc(
                "get_relationship_by_id_with_user",
                {
                    "p_relationship_id": relationship_id,
                    "p_current_user_id": current_user_id,
                },
            ).execute()

            if not response.data:
                return None

            return DBRelationshipWithUserResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error fetching relationship with user: {e}")
            return None

    async def get_user_relationships(
        self, *, user_id: str
    ) -> list[DBRelationshipResponse]:
        """Get all relationships for a user (legacy method for backward compatibility)"""
        try:
            query = self.relationships.select("*").or_(
                f"user_id_1.eq.{user_id},user_id_2.eq.{user_id}"
            )

            response = query.execute()
            if not response.data:
                return []

            return [DBRelationshipResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error fetching user relationships: {e}")
            return []

    async def get_user_relationships_with_users(
        self, *, user_id: str, skip: int = 0, take: int = 10
    ) -> DBRelationshipsListResponse:
        """Get relationships for a user with other user data and pagination"""
        try:
            response = self.supabase.rpc(
                "get_user_relationships",
                {
                    "p_user_id": user_id,
                    "p_skip": skip,
                    "p_take": take,
                },
            ).execute()

            if not response.data:
                return DBRelationshipsListResponse(relationships=[], total_count=0)

            relationships = []
            total_count = 0

            for item in response.data:
                relationships.append(DBRelationshipWithUserResponse(**item))
                total_count = item.get("total_count", 0)

            return DBRelationshipsListResponse(
                relationships=relationships, total_count=total_count
            )
        except Exception as e:
            logger.info(f"Error fetching user relationships with users: {e}")
            return DBRelationshipsListResponse(relationships=[], total_count=0)

    async def update_relationship(
        self, *, relationship_id: str
    ) -> DBRelationshipResponse | None:
        """Update a relationship"""
        try:
            update_data = {"updated_at": datetime.now().isoformat()}

            response = (
                self.relationships.update(update_data)
                .eq("id", relationship_id)
                .execute()
            )
            if not response.data:
                return None

            return DBRelationshipResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error updating relationship: {e}")
            return None

    async def delete_relationship(self, *, relationship_id: str) -> bool:
        """Delete a relationship"""
        try:
            response = self.relationships.delete().eq("id", relationship_id).execute()
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            logger.info(f"Error deleting relationship: {e}")
            return False

    async def check_existing_relationship(
        self, *, user_id_1: str, user_id_2: str
    ) -> DBRelationshipResponse | None:
        """Check if a relationship already exists between two users"""
        try:
            response = (
                self.relationships.select("*")
                .or_(
                    f"and(user_id_1.eq.{user_id_1},user_id_2.eq.{user_id_2}),"
                    f"and(user_id_1.eq.{user_id_2},user_id_2.eq.{user_id_1})"
                )
                .execute()
            )

            if not response.data:
                return None

            return DBRelationshipResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error checking existing relationship: {e}")
            return None
