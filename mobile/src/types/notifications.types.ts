import { BaseResponse, BaseListResponse, BasePaginatedListResponse } from './common.types';

// Notification Data Types
export interface NotificationData {
    id: string;
    user_id: string;
    title: string;
    message: string;
    type: 'relationship_request' | 'event_request' | 'event_reminder' | 'system';
    read: boolean;
    created_at: string;
    updated_at: string;
    metadata?: Record<string, any>;
}

// Notification State Types
export interface NotificationState {
    notifications: NotificationData[];
    unreadCount: number;
    loading: boolean;
    error: string | null;
}

// Notification Response Types
export interface NotificationResponse extends BaseResponse {
    notification: NotificationData;
}

export interface NotificationsListResponse
    extends BaseListResponse<NotificationData> {
    notifications: NotificationData[];
}

export interface NotificationsPaginatedListResponse
    extends BasePaginatedListResponse<NotificationData> {
    notifications: NotificationData[];
}

// Notification Filter Types
export interface NotificationFilters {
    type?: string;
    read?: boolean;
    dateRange?: {
        start: string;
        end: string;
    };
}