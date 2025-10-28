import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    SafeAreaView,
    Alert,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState, AppDispatch } from '../redux/store';
import { authActions } from '../redux/slices/auth.slice';
import { supabase } from '../lib/supabaseClient';
import { Ionicons } from '@expo/vector-icons';

const ProfileScreen = () => {
    const dispatch = useDispatch<AppDispatch>();
    const user = useSelector((state: RootState) => state.auth.session?.user);
    const relationships = useSelector((state: RootState) => state.relationships.relationships);
    const notifications = useSelector((state: RootState) => state.notifications.notifications);

    const handleSignOut = async () => {
        Alert.alert(
            'Sign Out',
            'Are you sure you want to sign out?',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Sign Out',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await supabase.auth.signOut();
                            dispatch(authActions.clearAuth());
                        } catch (error) {
                            Alert.alert('Error', 'Failed to sign out');
                        }
                    },
                },
            ]
        );
    };

    const handleEditProfile = () => {
        // TODO: Navigate to edit profile
        console.log('Edit profile');
    };

    const handleManageRelationships = () => {
        // TODO: Navigate to relationships management
        console.log('Manage relationships');
    };

    const handleViewNotifications = () => {
        // TODO: Navigate to notifications
        console.log('View notifications');
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Profile</Text>
                <TouchableOpacity style={styles.editButton} onPress={handleEditProfile}>
                    <Ionicons name="create" size={20} color="#4a90e2" />
                </TouchableOpacity>
            </View>

            <ScrollView style={styles.content}>
                <View style={styles.profileCard}>
                    <View style={styles.avatarContainer}>
                        <Ionicons name="person" size={48} color="#4a90e2" />
                    </View>
                    <Text style={styles.userName}>
                        {user?.user_metadata?.name || 'User'}
                    </Text>
                    <Text style={styles.userEmail}>{user?.email}</Text>
                </View>

                <View style={styles.statsContainer}>
                    <View style={styles.statItem}>
                        <Text style={styles.statNumber}>{relationships.length}</Text>
                        <Text style={styles.statLabel}>Relationships</Text>
                    </View>
                    <View style={styles.statItem}>
                        <Text style={styles.statNumber}>
                            {notifications.filter(n => !n.read).length}
                        </Text>
                        <Text style={styles.statLabel}>Unread</Text>
                    </View>
                </View>

                <View style={styles.menuSection}>
                    <TouchableOpacity style={styles.menuItem} onPress={handleManageRelationships}>
                        <Ionicons name="people" size={24} color="#4a90e2" />
                        <Text style={styles.menuItemText}>Manage Relationships</Text>
                        <Ionicons name="chevron-forward" size={20} color="#d4d4d4" />
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={handleViewNotifications}>
                        <Ionicons name="notifications" size={24} color="#4a90e2" />
                        <View style={styles.menuItemContent}>
                            <Text style={styles.menuItemText}>Notifications</Text>
                            {notifications.filter(n => !n.read).length > 0 && (
                                <View style={styles.badge}>
                                    <Text style={styles.badgeText}>
                                        {notifications.filter(n => !n.read).length}
                                    </Text>
                                </View>
                            )}
                        </View>
                        <Ionicons name="chevron-forward" size={20} color="#d4d4d4" />
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem}>
                        <Ionicons name="settings" size={24} color="#4a90e2" />
                        <Text style={styles.menuItemText}>Settings</Text>
                        <Ionicons name="chevron-forward" size={20} color="#d4d4d4" />
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem}>
                        <Ionicons name="help-circle" size={24} color="#4a90e2" />
                        <Text style={styles.menuItemText}>Help & Support</Text>
                        <Ionicons name="chevron-forward" size={20} color="#d4d4d4" />
                    </TouchableOpacity>
                </View>

                <View style={styles.signOutSection}>
                    <TouchableOpacity style={styles.signOutButton} onPress={handleSignOut}>
                        <Ionicons name="log-out" size={20} color="#ff6b6b" />
                        <Text style={styles.signOutButtonText}>Sign Out</Text>
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
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#e5e5e5',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#262626',
    },
    editButton: {
        padding: 8,
    },
    content: {
        flex: 1,
        padding: 24,
    },
    profileCard: {
        backgroundColor: 'white',
        padding: 24,
        borderRadius: 12,
        alignItems: 'center',
        marginBottom: 24,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 3.84,
        elevation: 5,
    },
    avatarContainer: {
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: '#e3f2fd',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 16,
    },
    userName: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#262626',
        marginBottom: 4,
    },
    userEmail: {
        fontSize: 14,
        color: '#525252',
    },
    statsContainer: {
        flexDirection: 'row',
        backgroundColor: 'white',
        borderRadius: 12,
        padding: 20,
        marginBottom: 24,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 3.84,
        elevation: 5,
    },
    statItem: {
        flex: 1,
        alignItems: 'center',
    },
    statNumber: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#4a90e2',
        marginBottom: 4,
    },
    statLabel: {
        fontSize: 12,
        color: '#525252',
    },
    menuSection: {
        backgroundColor: 'white',
        borderRadius: 12,
        marginBottom: 24,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 3.84,
        elevation: 5,
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingVertical: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#f5f5f5',
    },
    menuItemContent: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    menuItemText: {
        fontSize: 16,
        color: '#262626',
        marginLeft: 16,
        flex: 1,
    },
    badge: {
        backgroundColor: '#ff6b6b',
        borderRadius: 10,
        minWidth: 20,
        height: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginLeft: 8,
    },
    badgeText: {
        color: 'white',
        fontSize: 12,
        fontWeight: '600',
    },
    signOutSection: {
        marginBottom: 24,
    },
    signOutButton: {
        backgroundColor: 'white',
        borderWidth: 1,
        borderColor: '#ff6b6b',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 16,
        paddingHorizontal: 24,
        borderRadius: 8,
        gap: 8,
    },
    signOutButtonText: {
        color: '#ff6b6b',
        fontSize: 16,
        fontWeight: '600',
    },
    footer: {
        alignItems: 'center',
        paddingVertical: 16,
    },
    footerText: {
        fontSize: 12,
        color: '#d4d4d4',
    },
});

export default ProfileScreen;