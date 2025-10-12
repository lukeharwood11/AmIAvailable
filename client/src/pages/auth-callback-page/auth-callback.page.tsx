import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../../lib/supabaseClient';
import { storeAccessTokens } from '../../api/auth.api';
import LoadingIcon from '../../components/icons/LoadingIcon';
import { Note } from '../../components/note';
import styles from './auth-callback.page.module.css';

const AuthCallbackPage: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const handleAuthCallback = async () => {
            try {
                // Get the current session after OAuth redirect
                const {
                    data: { session },
                    error: sessionError,
                } = await supabase.auth.getSession();

                if (sessionError) {
                    throw new Error(`Session error: ${sessionError.message}`);
                }

                if (!session) {
                    throw new Error('No session found after OAuth callback');
                }

                // Extract Google provider data from session
                const user = session.user;
                if (!user) {
                    throw new Error('No user found in session');
                }

                console.log('Session: ', session);

                const accessToken = session.provider_token;
                const refreshToken = session.provider_refresh_token;

                if (accessToken && refreshToken) {
                    const storedTokens = await storeAccessTokens(
                        accessToken,
                        refreshToken,
                        user.id
                    );
                    if (!storedTokens) {
                        throw new Error('Failed to store Google tokens');
                    }
                    console.log(
                        'Successfully stored Google tokens for user:',
                        user.id
                    );
                }

                // Redirect to home page
                navigate('/dashboard', { replace: true });
            } catch (err) {
                console.error('Auth callback error:', err);
                setError(
                    err instanceof Error
                        ? err.message
                        : 'An error occurred during authentication'
                );
            } finally {
                setLoading(false);
            }
        };

        handleAuthCallback();
    }, [navigate]);

    if (loading) {
        return (
            <div className={styles.container}>
                <div className={styles.loadingBox}>
                    <LoadingIcon size={60} />
                    <p>Completing sign in...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className={styles.container}>
                <div className={styles.errorBox}>
                    <Note variant="error">{error}</Note>
                    <button
                        onClick={() => navigate('/login')}
                        className={styles.backButton}
                    >
                        Back to Login
                    </button>
                </div>
            </div>
        );
    }

    return null; // Should not reach here as we navigate away on success
};

export default AuthCallbackPage;
