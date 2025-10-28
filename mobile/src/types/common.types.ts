// Common data models shared across different hubs

// User Data Types
export interface UserData {
    id: string;
    email: string;
    full_name: string;
}

// API Response Types
export interface ApiResponse<T = any> {
    message: string;
    data?: T;
}

export interface ApiError {
    message: string;
    status?: number;
}

// Request State Types
export interface RequestState {
    loading: boolean;
    error: string | null;
}

// Pagination Types
export interface PaginationParams {
    skip?: number;
    take?: number;
}

export interface PaginationData {
    skip: number;
    take: number;
    total_count: number;
}

// Common Response Wrapper Types
export interface BaseResponse {
    status: string;
    message?: string;
}

export interface BaseListResponse<T> extends BaseResponse {
    count: number;
    filters?: Record<string, string | number>;
    // T is used for type safety in extending interfaces
    data?: T[];
}

export interface BasePaginatedListResponse<T> extends BaseListResponse<T> {
    total_count: number;
    skip: number;
    take: number;
}

// Common Request Types
export interface BaseCreateRequest {
    // Base interface for create requests
}

export interface BaseUpdateRequest {
    // Base interface for update requests
}

// Common Delete Response
export interface BaseDeleteResponse extends BaseResponse {
    message: string;
}