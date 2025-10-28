import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    SafeAreaView,
    ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

const LandingScreen = () => {
    const navigation = useNavigation();

    const handleLogin = () => {
        navigation.navigate('Login' as never);
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <View style={styles.heroSection}>
                    <View style={styles.logoContainer}>
                        <Ionicons name="calendar" size={80} color="#4a90e2" />
                        <Text style={styles.logoText}>AMIA</Text>
                    </View>
                    
                    <Text style={styles.title}>Am I Available?</Text>
                    <Text style={styles.subtitle}>
                        Coordinate your availability with friends and family effortlessly
                    </Text>
                </View>

                <View style={styles.featuresSection}>
                    <View style={styles.feature}>
                        <Ionicons name="people" size={40} color="#4a90e2" />
                        <Text style={styles.featureTitle}>Smart Scheduling</Text>
                        <Text style={styles.featureDescription}>
                            Automatically find the best times for everyone
                        </Text>
                    </View>

                    <View style={styles.feature}>
                        <Ionicons name="notifications" size={40} color="#8e44ad" />
                        <Text style={styles.featureTitle}>Real-time Updates</Text>
                        <Text style={styles.featureDescription}>
                            Stay informed about schedule changes instantly
                        </Text>
                    </View>

                    <View style={styles.feature}>
                        <Ionicons name="sync" size={40} color="#4a90e2" />
                        <Text style={styles.featureTitle}>Seamless Integration</Text>
                        <Text style={styles.featureDescription}>
                            Works with your existing calendar apps
                        </Text>
                    </View>
                </View>

                <View style={styles.ctaSection}>
                    <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
                        <Text style={styles.loginButtonText}>Get Started</Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.footer}>
                    <Text style={styles.footerText}>
                        Made with ❤️ by AMIA's brother
                    </Text>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8f9fa',
    },
    scrollContent: {
        flexGrow: 1,
    },
    heroSection: {
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingVertical: 60,
    },
    logoContainer: {
        alignItems: 'center',
        marginBottom: 24,
    },
    logoText: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#4a90e2',
        marginTop: 8,
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#262626',
        textAlign: 'center',
        marginBottom: 12,
    },
    subtitle: {
        fontSize: 16,
        color: '#525252',
        textAlign: 'center',
        lineHeight: 24,
    },
    featuresSection: {
        paddingHorizontal: 24,
        paddingVertical: 40,
    },
    feature: {
        alignItems: 'center',
        marginBottom: 32,
    },
    featureTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
        marginTop: 12,
        marginBottom: 8,
    },
    featureDescription: {
        fontSize: 14,
        color: '#525252',
        textAlign: 'center',
        lineHeight: 20,
    },
    ctaSection: {
        paddingHorizontal: 24,
        paddingVertical: 40,
    },
    loginButton: {
        backgroundColor: '#4a90e2',
        paddingVertical: 16,
        paddingHorizontal: 32,
        borderRadius: 8,
        alignItems: 'center',
    },
    loginButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
    footer: {
        alignItems: 'center',
        paddingVertical: 24,
    },
    footerText: {
        fontSize: 14,
        color: '#525252',
    },
});

export default LandingScreen;