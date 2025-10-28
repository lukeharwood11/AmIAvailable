import { supabase } from '../lib/supabaseClient';

export interface UserTokens {
    id: string;
    google_access_token: string;
    google_refresh_token: string;
}

export const storeAccessTokens = async (
    googleAccessToken: string,
    googleRefreshToken: string,
    userId: string
): Promise<UserTokens | null> => {
    try {
        console.log('Storing Google tokens for user:', userId);
        console.log('Google access token:', googleAccessToken);
        console.log('Google refresh token:', googleRefreshToken);
        const { data, error } = await supabase
            .from('user_tokens')
            .upsert({
                id: userId,
                google_access_token: googleAccessToken,
                google_refresh_token: googleRefreshToken,
            })
            .select()
            .single();
        if (error) {
            throw error;
        }
        return data;
    } catch (error) {
        // TODO: fix error
        console.log(error);
        return null;
    }
};

export interface GetAccessTokensResponse {
    google_access_token: string;
    google_refresh_token: string;
}

export const getAccessTokens = async (
    userId: string
): Promise<GetAccessTokensResponse | null> => {
    try {
        const { data, error } = await supabase
            .from('user_tokens')
            .select('google_access_token, google_refresh_token')
            .eq('id', userId)
            .single();
        if (error) {
            throw error;
        }
        return data as GetAccessTokensResponse;
    } catch (error) {
        // TODO: fix error
        console.log(error);
        return null;
    }
};