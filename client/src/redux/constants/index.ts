export * from './api.constants';

// Action Status Constants
export const ACTION_STATUS = {
    IDLE: 'idle',
    LOADING: 'loading',
    SUCCEEDED: 'succeeded',
    FAILED: 'failed',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
    AUTH: {
        LOGIN_FAILED: 'Login failed. Please try again.',
        LOGOUT_FAILED: 'Logout failed. Please try again.',
        TOKEN_REFRESH_FAILED: 'Session expired. Please login again.',
        UNAUTHORIZED: 'Unauthorized access. Please login.',
    },
    RECIPE: {
        FETCH_FAILED: 'Failed to fetch recipes.',
        CREATE_FAILED: 'Failed to create recipe.',
        UPDATE_FAILED: 'Failed to update recipe.',
        DELETE_FAILED: 'Failed to delete recipe.',
        SEARCH_FAILED: 'Failed to search recipes.',
    },
    CALENDAR: {
        FETCH_EVENTS_FAILED: 'Failed to fetch calendar events.',
        SYNC_FAILED: 'Failed to sync with Google Calendar.',
    },
    RELATIONSHIPS: {
        CREATE_FAILED: 'Failed to create relationship.',
        FETCH_FAILED: 'Failed to fetch relationships.',
        UPDATE_FAILED: 'Failed to update relationship.',
        DELETE_FAILED: 'Failed to delete relationship.',
        APPROVE_FAILED: 'Failed to approve relationship.',
        REJECT_FAILED: 'Failed to reject relationship.',
    },
    RELATIONSHIP_REQUESTS: {
        CREATE_FAILED: 'Failed to create relationship request.',
        FETCH_FAILED: 'Failed to fetch relationship requests.',
        UPDATE_FAILED: 'Failed to update relationship request.',
        DELETE_FAILED: 'Failed to delete relationship request.',
        APPROVE_FAILED: 'Failed to approve relationship request.',
        REJECT_FAILED: 'Failed to reject relationship request.',
    },
    EVENT_REQUESTS: {
        CREATE_FAILED: 'Failed to create event request.',
        FETCH_FAILED: 'Failed to fetch event requests.',
        UPDATE_FAILED: 'Failed to update event request.',
        DELETE_FAILED: 'Failed to delete event request.',
    },
    NOTIFICATIONS: {
        CREATE_FAILED: 'Failed to create notification.',
        FETCH_FAILED: 'Failed to fetch notifications.',
        UPDATE_FAILED: 'Failed to update notification.',
        DELETE_FAILED: 'Failed to delete notification.',
        MARK_ALL_READ_FAILED: 'Failed to mark all notifications as read.',
    },
    AGENT: {
        CHAT_FAILED: 'Failed to chat with Amia. Please try again.',
        STREAMING_FAILED: 'Failed to stream response from Amia.',
    },
    AI_USAGE: {
        FETCH_FAILED: 'Failed to fetch AI usage data.',
        FETCH_COST_FAILED: 'Failed to fetch AI usage cost data.',
        REFRESH_FAILED: 'Failed to refresh AI usage data.',
    },
    GENERAL: {
        REQUEST_FAILED: 'Request failed. Please try again.',
    },
    NETWORK: {
        CONNECTION_ERROR:
            'Network connection error. Please check your internet connection.',
        SERVER_ERROR: 'Server error. Please try again later.',
        TIMEOUT: 'Request timeout. Please try again.',
    },
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
    AUTH_TOKEN: 'auth_token',
    REFRESH_TOKEN: 'refresh_token',
    USER_PREFERENCES: 'user_preferences',
} as const;
