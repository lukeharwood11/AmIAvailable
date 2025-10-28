import {
    UserData,
    BaseResponse,
    BaseListResponse,
    BasePaginatedListResponse,
    BaseCreateRequest,
    BaseUpdateRequest,
    BaseDeleteResponse,
} from './common.types';

// Event Request Data Types
export interface EventRequestData {
    id: string;
    requester_id: string;
    requested_id: string;
    event_id: string;
    status: 'pending' | 'accepted' | 'rejected';
    created_at: string;
    updated_at: string;
}

export interface EventRequestWithUserData {
    id: string;
    requester_id: string;
    requested_id: string;
    event_id: string;
    status: 'pending' | 'accepted' | 'rejected';
    created_at: string;
    updated_at: string;
    other_user: UserData;
}

// Event Request Types
export interface CreateEventRequestRequest extends BaseCreateRequest {
    requested_id: string;
    event_id: string;
}

export interface UpdateEventRequestRequest extends BaseUpdateRequest {
    status: 'accepted' | 'rejected';
}

// Event Request Response Types
export interface EventRequestResponse extends BaseResponse {
    event_request: EventRequestData;
}

export interface EventRequestWithUserResponse extends BaseResponse {
    event_request: EventRequestWithUserData;
}

export interface EventRequestsListResponse
    extends BaseListResponse<EventRequestData> {
    event_requests: EventRequestData[];
}

export interface EventRequestsWithUsersListResponse
    extends BasePaginatedListResponse<EventRequestWithUserData> {
    event_requests: EventRequestWithUserData[];
}

export interface EventRequestDeleteResponse extends BaseDeleteResponse {}

export interface EventRequestCreateResponse extends BaseResponse {
    event_request: EventRequestData;
}

export interface EventRequestUpdateResponse extends BaseResponse {
    event_request: EventRequestData;
}