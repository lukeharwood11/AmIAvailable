from fastapi import HTTPException
from ..databridge.relationships_databridge import (
    RelationshipsDatabridge,
    DBRelationshipResponse,
    DBRelationshipWithUserResponse,
)
from api.models.v1.relationships import (
    RelationshipData,
    RelationshipCreateResponse,
    RelationshipUpdateResponse,
    RelationshipDeleteResponse,
    RelationshipsListResponse,
    RelationshipResponse,
    RelationshipWithUserData,
    RelationshipWithUserResponse,
    RelationshipsWithUsersListResponse,
    UserData,
)


class RelationshipsService:
    def __init__(self, databridge: RelationshipsDatabridge) -> None:
        self.databridge: RelationshipsDatabridge = databridge

    def _convert_db_to_model(
        self, db_relationship: DBRelationshipResponse
    ) -> RelationshipData:
        """Convert database response to API model"""
        return RelationshipData(
            id=db_relationship.id,
            user_id_1=db_relationship.user_id_1,
            user_id_2=db_relationship.user_id_2,
            created_at=db_relationship.created_at,
            updated_at=db_relationship.updated_at,
        )

    def _convert_db_with_user_to_model(
        self, db_relationship: DBRelationshipWithUserResponse
    ) -> RelationshipWithUserData:
        """Convert database response with user data to API model"""
        return RelationshipWithUserData(
            id=db_relationship.id,
            user_id_1=db_relationship.user_id_1,
            user_id_2=db_relationship.user_id_2,
            created_at=db_relationship.created_at,
            updated_at=db_relationship.updated_at,
            other_user=UserData(
                id=db_relationship.other_user_id,
                email=db_relationship.other_user_email,
                full_name=db_relationship.other_user_full_name,
            ),
        )

    async def search_relationships(
        self, *, query: str, user_id: str
    ) -> RelationshipsListResponse:
        """Search for relationships by query"""
        db_relationships = await self.databridge.search_relationships(
            query=query, user_id=user_id
        )
        relationships = [
            self._convert_db_with_user_to_model(rel) for rel in db_relationships
        ]
        return RelationshipsListResponse(
            relationships=relationships, count=len(relationships), filters=None
        )

    async def create_relationship(
        self, *, user_id_1: str, user_id_2: str
    ) -> RelationshipCreateResponse:
        """Create a new relationship between two users"""
        # Check if relationship already exists
        existing = await self.databridge.check_existing_relationship(
            user_id_1=user_id_1, user_id_2=user_id_2
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Relationship already exists between these users",
            )

        # Create the relationship
        db_relationship = await self.databridge.create_relationship(
            user_id_1=user_id_1, user_id_2=user_id_2
        )

        if not db_relationship:
            raise HTTPException(status_code=500, detail="Failed to create relationship")

        relationship_data = self._convert_db_to_model(db_relationship)
        return RelationshipCreateResponse(relationship=relationship_data)

    async def get_relationship(self, *, relationship_id: str) -> RelationshipResponse:
        """Get a specific relationship by ID (legacy method)"""
        db_relationship = await self.databridge.get_relationship_by_id(
            relationship_id=relationship_id
        )

        if not db_relationship:
            raise HTTPException(status_code=404, detail="Relationship not found")

        relationship_data = self._convert_db_to_model(db_relationship)
        return RelationshipResponse(relationship=relationship_data)

    async def get_relationship_with_user(
        self, *, relationship_id: str, current_user_id: str
    ) -> RelationshipWithUserResponse:
        """Get a specific relationship by ID with other user data"""
        db_relationship = await self.databridge.get_relationship_by_id_with_user(
            relationship_id=relationship_id, current_user_id=current_user_id
        )

        if not db_relationship:
            raise HTTPException(status_code=404, detail="Relationship not found")

        relationship_data = self._convert_db_with_user_to_model(db_relationship)
        return RelationshipWithUserResponse(relationship=relationship_data)

    async def get_user_relationships(
        self, *, user_id: str
    ) -> RelationshipsListResponse:
        """Get all relationships for a user (legacy method)"""
        print(self.databridge)
        db_relationships = await self.databridge.get_user_relationships(user_id=user_id)

        relationships = [self._convert_db_to_model(rel) for rel in db_relationships]

        return RelationshipsListResponse(
            relationships=relationships, count=len(relationships), filters=None
        )

    async def get_user_relationships_with_users(
        self, *, user_id: str, skip: int = 0, take: int = 10
    ) -> RelationshipsWithUsersListResponse:
        """Get relationships for a user with other user data and pagination"""
        db_result = await self.databridge.get_user_relationships_with_users(
            user_id=user_id, skip=skip, take=take
        )

        relationships = [
            self._convert_db_with_user_to_model(rel) for rel in db_result.relationships
        ]

        return RelationshipsWithUsersListResponse(
            relationships=relationships,
            total_count=db_result.total_count,
            skip=skip,
            take=take,
        )

    async def update_relationship(
        self, *, relationship_id: str, user_id: str
    ) -> RelationshipUpdateResponse:
        """Update a relationship"""
        # First verify the relationship exists and user has permission
        existing = await self.databridge.get_relationship_by_id(
            relationship_id=relationship_id
        )

        if not existing:
            raise HTTPException(status_code=404, detail="Relationship not found")

        # Check if user is part of this relationship
        if existing.user_id_1 != user_id and existing.user_id_2 != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this relationship",
            )

        # Update the relationship
        db_relationship = await self.databridge.update_relationship(
            relationship_id=relationship_id
        )

        if not db_relationship:
            raise HTTPException(status_code=500, detail="Failed to update relationship")

        relationship_data = self._convert_db_to_model(db_relationship)
        return RelationshipUpdateResponse(relationship=relationship_data)

    async def delete_relationship(
        self, *, relationship_id: str, user_id: str
    ) -> RelationshipDeleteResponse:
        """Delete a relationship"""
        # First verify the relationship exists and user has permission
        existing = await self.databridge.get_relationship_by_id(
            relationship_id=relationship_id
        )

        if not existing:
            raise HTTPException(status_code=404, detail="Relationship not found")

        # Check if user is part of this relationship
        if existing.user_id_1 != user_id and existing.user_id_2 != user_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this relationship",
            )

        # Delete the relationship
        success = await self.databridge.delete_relationship(
            relationship_id=relationship_id
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete relationship")

        return RelationshipDeleteResponse()
