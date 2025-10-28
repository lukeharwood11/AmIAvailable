import { Session } from '@supabase/supabase-js';

// Auth State Types
export interface AuthState {
    session: Session | null;
    loading: boolean;
    isAuthenticated: boolean;
    accessToken: string | null;
    refreshToken: string | null;
    error: string | null;
}

// User Tokens Types
export interface UserTokens {
    id: string;
    google_access_token: string;
    google_refresh_token: string;
}

export interface GetAccessTokensResponse {
    google_access_token: string;
    google_refresh_token: string;
}