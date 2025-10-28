import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    SafeAreaView,
    Alert,
    ActivityIndicator,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../redux/store';
import { supabase } from '../lib/supabaseClient';
import { authActions } from '../redux/slices/auth.slice';
import { Ionicons } from '@expo/vector-icons';

const LoginScreen = () => {
    const navigation = useNavigation();
    const dispatch = useDispatch<AppDispatch>();
    const [loading, setLoading] = useState(false);

    const handleGoogleLogin = async () => {
        try {
            setLoading(true);
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: 'am-i-available://auth/callback',
                },
            });

            if (error) {
                Alert.alert('Error', error.message);
            }
        } catch (error) {
            Alert.alert('Error', 'Failed to sign in with Google');
        } finally {
            setLoading(false);
        }
    };

    const handleBack = () => {
        navigation.goBack();
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={handleBack} style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="#4a90e2" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Sign In</Text>
                <View style={styles.placeholder} />
            </View>

            <View style={styles.content}>
                <View style={styles.logoContainer}>
                    <Ionicons name="calendar" size={60} color="#4a90e2" />
                    <Text style={styles.logoText}>AMIA</Text>
                </View>

                <Text style={styles.title}>Welcome Back</Text>
                <Text style={styles.subtitle}>
                    Sign in to continue coordinating your availability
                </Text>

                <View style={styles.loginSection}>
                    <TouchableOpacity
                        style={[styles.googleButton, loading && styles.buttonDisabled]}
                        onPress={handleGoogleLogin}
                        disabled={loading}
                    >
                        {loading ? (
                            <ActivityIndicator color="white" />
                        ) : (
                            <>
                                <Ionicons name="logo-google" size={20} color="white" />
                                <Text style={styles.googleButtonText}>
                                    Continue with Google
                                </Text>
                            </>
                        )}
                    </TouchableOpacity>
                </View>

                <View style={styles.footer}>
                    <Text style={styles.footerText}>
                        By signing in, you agree to our Terms of Service and Privacy Policy
                    </Text>
                </View>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8f9fa',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#e5e5e5',
    },
    backButton: {
        padding: 8,
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
    },
    placeholder: {
        width: 40,
    },
    content: {
        flex: 1,
        paddingHorizontal: 24,
        paddingVertical: 40,
        alignItems: 'center',
    },
    logoContainer: {
        alignItems: 'center',
        marginBottom: 32,
    },
    logoText: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#4a90e2',
        marginTop: 8,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#262626',
        marginBottom: 8,
    },
    subtitle: {
        fontSize: 16,
        color: '#525252',
        textAlign: 'center',
        marginBottom: 48,
        lineHeight: 24,
    },
    loginSection: {
        width: '100%',
        marginBottom: 32,
    },
    googleButton: {
        backgroundColor: '#4a90e2',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 16,
        paddingHorizontal: 24,
        borderRadius: 8,
        gap: 12,
    },
    buttonDisabled: {
        opacity: 0.6,
    },
    googleButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
    footer: {
        alignItems: 'center',
    },
    footerText: {
        fontSize: 12,
        color: '#525252',
        textAlign: 'center',
        lineHeight: 18,
    },
});

export default LoginScreen;