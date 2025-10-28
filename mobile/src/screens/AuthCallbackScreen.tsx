import React, { useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ActivityIndicator,
    SafeAreaView,
} from 'react-native';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../redux/store';
import { authActions } from '../redux/slices/auth.slice';
import { supabase } from '../lib/supabaseClient';
import * as Linking from 'expo-linking';

const AuthCallbackScreen = () => {
    const dispatch = useDispatch<AppDispatch>();

    useEffect(() => {
        const handleAuthCallback = async () => {
            try {
                // Get the current session first
                const { data: { session }, error: sessionError } = await supabase.auth.getSession();
                
                if (sessionError) {
                    console.error('Session error:', sessionError);
                    dispatch(authActions.setAuthError(sessionError.message));
                    return;
                }

                if (session) {
                    dispatch(authActions.setSession({ session }));
                    return;
                }

                // If no session, try to get from URL
                const url = await Linking.getInitialURL();
                if (url) {
                    const { data, error } = await supabase.auth.getSessionFromUrl(url);
                    
                    if (error) {
                        console.error('Auth callback error:', error);
                        dispatch(authActions.setAuthError(error.message));
                    } else if (data.session) {
                        dispatch(authActions.setSession({ session: data.session }));
                    }
                } else {
                    // No URL and no session, set loading to false
                    dispatch(authActions.setLoading(false));
                }
            } catch (error) {
                console.error('Auth callback error:', error);
                dispatch(authActions.setAuthError('Authentication failed'));
            }
        };

        handleAuthCallback();
    }, [dispatch]);

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.content}>
                <ActivityIndicator size="large" color="#4a90e2" />
                <Text style={styles.text}>Completing sign in...</Text>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8f9fa',
    },
    content: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 24,
    },
    text: {
        fontSize: 16,
        color: '#525252',
        marginTop: 16,
    },
});

export default AuthCallbackScreen;