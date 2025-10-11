from fastapi import HTTPException
from ..databridge.relationship_metadata_databridge import (
    RelationshipMetadataDatabridge,
    DBRelationshipMetadataResponse,
)
from ..models.v1.relationship_metadata import (
    RelationshipMetadataData,
    RelationshipMetadataCreateResponse,
    RelationshipMetadataUpdateResponse,
    RelationshipMetadataDeleteResponse,
    RelationshipMetadataListResponse,
    RelationshipMetadataResponse,
)


class RelationshipMetadataService:
    def __init__(self, databridge: RelationshipMetadataDatabridge) -> None:
        self.databridge = databridge

    def _convert_db_to_model(
        self, db_metadata: DBRelationshipMetadataResponse
    ) -> RelationshipMetadataData:
        """Convert database response to API model"""
        return RelationshipMetadataData(
            id=db_metadata.id,
            user_id=db_metadata.user_id,
            relationship_id=db_metadata.relationship_id,
            relationship_type=db_metadata.relationship_type,
            created_at=db_metadata.created_at,
            updated_at=db_metadata.updated_at,
        )

    async def create_relationship_metadata(
        self, *, user_id: str, relationship_id: str, relationship_type: str
    ) -> RelationshipMetadataCreateResponse:
        """Create new relationship metadata"""
        # Check if metadata already exists for this user and relationship
        existing = await self.databridge.check_existing_metadata(
            user_id=user_id, relationship_id=relationship_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Relationship metadata already exists for this user and relationship",
            )

        # Create the metadata
        db_metadata = await self.databridge.create_relationship_metadata(
            user_id=user_id,
            relationship_id=relationship_id,
            relationship_type=relationship_type,
        )

        if not db_metadata:
            raise HTTPException(
                status_code=500, detail="Failed to create relationship metadata"
            )

        metadata_data = self._convert_db_to_model(db_metadata)
        return RelationshipMetadataCreateResponse(relationship_metadata=metadata_data)

    async def get_relationship_metadata(
        self, *, metadata_id: str
    ) -> RelationshipMetadataResponse:
        """Get specific relationship metadata by ID"""
        db_metadata = await self.databridge.get_relationship_metadata_by_id(
            metadata_id=metadata_id
        )

        if not db_metadata:
            raise HTTPException(
                status_code=404, detail="Relationship metadata not found"
            )

        metadata_data = self._convert_db_to_model(db_metadata)
        return RelationshipMetadataResponse(relationship_metadata=metadata_data)

    async def get_user_relationship_metadata(
        self,
        *,
        user_id: str,
        relationship_id: str | None = None,
        relationship_type: str | None = None,
    ) -> RelationshipMetadataListResponse:
        """Get all relationship metadata for a user with optional filters"""
        db_metadata_list = await self.databridge.get_user_relationship_metadata(
            user_id=user_id,
            relationship_id=relationship_id,
            relationship_type=relationship_type,
        )

        metadata_list = [
            self._convert_db_to_model(metadata) for metadata in db_metadata_list
        ]

        filters: dict[str, str] = {}
        if relationship_id:
            filters["relationship_id"] = relationship_id
        if relationship_type:
            filters["relationship_type"] = relationship_type

        return RelationshipMetadataListResponse(
            relationship_metadata=metadata_list,
            count=len(metadata_list),
            filters=filters if filters else None,
        )

    async def get_relationship_metadata_by_relationship(
        self, *, relationship_id: str
    ) -> RelationshipMetadataListResponse:
        """Get all metadata for a specific relationship"""
        db_metadata_list = (
            await self.databridge.get_relationship_metadata_by_relationship(
                relationship_id=relationship_id
            )
        )

        metadata_list = [
            self._convert_db_to_model(metadata) for metadata in db_metadata_list
        ]

        return RelationshipMetadataListResponse(
            relationship_metadata=metadata_list,
            count=len(metadata_list),
            filters={"relationship_id": relationship_id},
        )

    async def update_relationship_metadata(
        self, *, metadata_id: str, user_id: str, relationship_type: str
    ) -> RelationshipMetadataUpdateResponse:
        """Update relationship metadata"""
        # First verify the metadata exists and user has permission
        existing = await self.databridge.get_relationship_metadata_by_id(
            metadata_id=metadata_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Relationship metadata not found"
            )

        # Check if user owns this metadata
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this metadata",
            )

        # Update the metadata
        db_metadata = await self.databridge.update_relationship_metadata(
            metadata_id=metadata_id, relationship_type=relationship_type
        )

        if not db_metadata:
            raise HTTPException(
                status_code=500, detail="Failed to update relationship metadata"
            )

        metadata_data = self._convert_db_to_model(db_metadata)
        return RelationshipMetadataUpdateResponse(relationship_metadata=metadata_data)

    async def delete_relationship_metadata(
        self, *, metadata_id: str, user_id: str
    ) -> RelationshipMetadataDeleteResponse:
        """Delete relationship metadata"""
        # First verify the metadata exists and user has permission
        existing = await self.databridge.get_relationship_metadata_by_id(
            metadata_id=metadata_id
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Relationship metadata not found"
            )

        # Check if user owns this metadata
        if existing.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this metadata",
            )

        # Delete the metadata
        success = await self.databridge.delete_relationship_metadata(
            metadata_id=metadata_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete relationship metadata"
            )

        return RelationshipMetadataDeleteResponse()

    async def delete_relationship_metadata_by_relationship(
        self, *, relationship_id: str
    ) -> RelationshipMetadataDeleteResponse:
        """Delete all metadata for a specific relationship (used when deleting relationship)"""
        success = await self.databridge.delete_relationship_metadata_by_relationship(
            relationship_id=relationship_id
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete relationship metadata"
            )

        return RelationshipMetadataDeleteResponse()
