import { useState } from 'react';
import { supabase } from '../../lib/supabaseClient';
import Button from '../../components/button/Button';
import { Note } from '../../components/note';
import { GoogleIcon, Logo } from '../../components/icons';
import styles from './login.page.module.css';

const LoginPage = () => {
    const [error, setError] = useState<string | null>(null);

    const handleGoogleLogin = async () => {
        try {
            const { error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    scopes: 'email profile openid https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/calendar',
                    queryParams: {
                        access_type: 'offline',
                        prompt: 'consent',
                    },
                    redirectTo: `${window.location.origin}/auth/callback`,
                },
            });
            if (error) throw error;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : 'An error occurred during Google login'
            );
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.loginBox}>
                <div className={styles.header}>
                    <Logo size={50} />
                    <h1>Welcome!</h1>
                </div>
                {error && <Note variant="error">{error}</Note>}

                <Button
                    onClick={handleGoogleLogin}
                    variant='secondary-subtle'
                    fullWidth
                    leftIcon={<GoogleIcon size={18} />}
                >
                    Sign in with Google
                </Button>

                <p className={styles.signupLink}>
                    Don't have an account? Create one above!
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
