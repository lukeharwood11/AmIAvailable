import {
    UserData,
    BaseResponse,
    BaseListResponse,
    BasePaginatedListResponse,
    BaseCreateRequest,
    BaseUpdateRequest,
    BaseDeleteResponse,
} from './common.types';

// Relationship Request Data Types
export interface RelationshipRequestData {
    id: string;
    requester_id: string;
    requested_id: string;
    status: 'pending' | 'accepted' | 'rejected';
    created_at: string;
    updated_at: string;
}

export interface RelationshipRequestWithUserData {
    id: string;
    requester_id: string;
    requested_id: string;
    status: 'pending' | 'accepted' | 'rejected';
    created_at: string;
    updated_at: string;
    other_user: UserData;
}

// Relationship Request Types
export interface CreateRelationshipRequestRequest extends BaseCreateRequest {
    requested_id: string;
}

export interface UpdateRelationshipRequestRequest extends BaseUpdateRequest {
    status: 'accepted' | 'rejected';
}

// Relationship Request Response Types
export interface RelationshipRequestResponse extends BaseResponse {
    relationship_request: RelationshipRequestData;
}

export interface RelationshipRequestWithUserResponse extends BaseResponse {
    relationship_request: RelationshipRequestWithUserData;
}

export interface RelationshipRequestsListResponse
    extends BaseListResponse<RelationshipRequestData> {
    relationship_requests: RelationshipRequestData[];
}

export interface RelationshipRequestsWithUsersListResponse
    extends BasePaginatedListResponse<RelationshipRequestWithUserData> {
    relationship_requests: RelationshipRequestWithUserData[];
}

export interface RelationshipRequestDeleteResponse extends BaseDeleteResponse {}

export interface RelationshipRequestCreateResponse extends BaseResponse {
    relationship_request: RelationshipRequestData;
}

export interface RelationshipRequestUpdateResponse extends BaseResponse {
    relationship_request: RelationshipRequestData;
}