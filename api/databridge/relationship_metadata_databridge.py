from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DBRelationshipMetadataResponse(BaseModel):
    id: str
    user_id: str
    relationship_id: str
    relationship_type: str
    created_at: datetime
    updated_at: datetime


class RelationshipMetadataDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.relationship_metadata = self.supabase.table("relationship_metadata")

    async def create_relationship_metadata(
        self, *, user_id: str, relationship_id: str, relationship_type: str
    ) -> DBRelationshipMetadataResponse | None:
        """Create new relationship metadata"""
        try:
            data = {
                "user_id": user_id,
                "relationship_id": relationship_id,
                "relationship_type": relationship_type,
            }

            response = self.relationship_metadata.insert(data).execute()
            if not response.data:
                return None

            _data = response.data[0]
            return DBRelationshipMetadataResponse(**_data)
        except Exception as e:
            logger.info(f"Error creating relationship metadata: {e}")
            return None

    async def get_relationship_metadata_by_id(
        self, *, metadata_id: str
    ) -> DBRelationshipMetadataResponse | None:
        """Get specific relationship metadata by ID"""
        try:
            response = (
                self.relationship_metadata.select("*")
                .eq("id", metadata_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            return DBRelationshipMetadataResponse(**response.data)
        except Exception as e:
            logger.info(f"Error fetching relationship metadata: {e}")
            return None

    async def get_user_relationship_metadata(
        self,
        *,
        user_id: str,
        relationship_id: str | None = None,
        relationship_type: str | None = None,
    ) -> list[DBRelationshipMetadataResponse]:
        """Get all relationship metadata for a user with optional filters"""
        try:
            query = self.relationship_metadata.select("*").eq("user_id", user_id)

            if relationship_id:
                query = query.eq("relationship_id", relationship_id)
            if relationship_type:
                query = query.eq("relationship_type", relationship_type)

            response = query.execute()
            if not response.data:
                return []

            return [DBRelationshipMetadataResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error fetching user relationship metadata: {e}")
            return []

    async def get_relationship_metadata_by_relationship(
        self, *, relationship_id: str
    ) -> list[DBRelationshipMetadataResponse]:
        """Get all metadata for a specific relationship"""
        try:
            response = (
                self.relationship_metadata.select("*")
                .eq("relationship_id", relationship_id)
                .execute()
            )
            if not response.data:
                return []

            return [DBRelationshipMetadataResponse(**item) for item in response.data]
        except Exception as e:
            logger.info(f"Error fetching relationship metadata by relationship: {e}")
            return []

    async def update_relationship_metadata(
        self, *, metadata_id: str, relationship_type: str
    ) -> DBRelationshipMetadataResponse | None:
        """Update relationship metadata"""
        try:
            update_data = {
                "relationship_type": relationship_type,
                "updated_at": datetime.now().isoformat(),
            }

            response = (
                self.relationship_metadata.update(update_data)
                .eq("id", metadata_id)
                .execute()
            )
            if not response.data:
                return None

            return DBRelationshipMetadataResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error updating relationship metadata: {e}")
            return None

    async def delete_relationship_metadata(self, *, metadata_id: str) -> bool:
        """Delete relationship metadata"""
        try:
            response = (
                self.relationship_metadata.delete().eq("id", metadata_id).execute()
            )
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            logger.info(f"Error deleting relationship metadata: {e}")
            return False

    async def delete_relationship_metadata_by_relationship(
        self, *, relationship_id: str
    ) -> bool:
        """Delete all metadata for a specific relationship"""
        try:
            response = (
                self.relationship_metadata.delete()
                .eq("relationship_id", relationship_id)
                .execute()
            )
            return response.data is not None
        except Exception as e:
            logger.info(f"Error deleting relationship metadata by relationship: {e}")
            return False

    async def check_existing_metadata(
        self, *, user_id: str, relationship_id: str
    ) -> DBRelationshipMetadataResponse | None:
        """Check if metadata already exists for user and relationship"""
        try:
            response = (
                self.relationship_metadata.select("*")
                .eq("user_id", user_id)
                .eq("relationship_id", relationship_id)
                .execute()
            )

            if not response.data:
                return None

            return DBRelationshipMetadataResponse(**response.data[0])
        except Exception as e:
            logger.info(f"Error checking existing metadata: {e}")
            return None
