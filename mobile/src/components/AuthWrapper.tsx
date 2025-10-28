import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { authActions } from '../redux/slices/auth.slice';
import { supabase } from '../lib/supabaseClient';
import { View, ActivityIndicator, StyleSheet } from 'react-native';

interface AuthWrapperProps {
    children: React.ReactNode;
}

const AuthWrapper: React.FC<AuthWrapperProps> = ({ children }) => {
    const dispatch = useDispatch<AppDispatch>();
    const { loading, isAuthenticated } = useSelector((state: RootState) => state.auth);

    useEffect(() => {
        // Check for existing session on app start
        const checkSession = async () => {
            try {
                const { data: { session }, error } = await supabase.auth.getSession();
                
                if (error) {
                    console.error('Session check error:', error);
                    dispatch(authActions.setAuthError(error.message));
                } else {
                    dispatch(authActions.setSession({ session }));
                }
            } catch (error) {
                console.error('Session check error:', error);
                dispatch(authActions.setAuthError('Failed to check authentication'));
            }
        };

        checkSession();

        // Listen for auth state changes
        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                console.log('Auth state changed:', event, session?.user?.email);
                dispatch(authActions.setSession({ session }));
            }
        );

        return () => {
            subscription.unsubscribe();
        };
    }, [dispatch]);

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#4a90e2" />
            </View>
        );
    }

    return <>{children}</>;
};

const styles = StyleSheet.create({
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f8f9fa',
    },
});

export default AuthWrapper;