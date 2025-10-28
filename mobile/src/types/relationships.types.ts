import {
    UserData,
    BaseResponse,
    BaseListResponse,
    BasePaginatedListResponse,
    BaseCreateRequest,
    BaseUpdateRequest,
    BaseDeleteResponse,
} from './common.types';

// Relationship Data Types
export interface RelationshipData {
    id: string;
    user_id_1: string;
    user_id_2: string;
    created_at: string;
    updated_at: string;
}

export interface RelationshipWithUserData {
    id: string;
    user_id_1: string;
    user_id_2: string;
    created_at: string;
    updated_at: string;
    other_user: UserData;
}

// Relationship Request Types
export interface CreateRelationshipRequest extends BaseCreateRequest {
    user_id_2: string;
}

export interface UpdateRelationshipRequest extends BaseUpdateRequest {
    relationship_type?: string;
    status?: string;
}

// Relationship Response Types
export interface RelationshipResponse extends BaseResponse {
    relationship: RelationshipData;
}

export interface RelationshipWithUserResponse extends BaseResponse {
    relationship: RelationshipWithUserData;
}

export interface RelationshipsListResponse
    extends BaseListResponse<RelationshipData> {
    relationships: RelationshipData[];
}

export interface RelationshipsWithUsersListResponse
    extends BasePaginatedListResponse<RelationshipWithUserData> {
    relationships: RelationshipWithUserData[];
}

export interface RelationshipDeleteResponse extends BaseDeleteResponse {}

export interface RelationshipCreateResponse extends BaseResponse {
    relationship: RelationshipData;
}

export interface RelationshipUpdateResponse extends BaseResponse {
    relationship: RelationshipData;
}

// Re-export types that are used in the state but defined in relationship-requests.types.ts
export type {
    RelationshipRequestData,
    RelationshipRequestWithUserData,
} from './relationship-requests.types';