import React, { useEffect, useCallback } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    SafeAreaView,
    RefreshControl,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { Ionicons } from '@expo/vector-icons';

const HomeScreen = () => {
    const dispatch = useDispatch<AppDispatch>();
    const user = useSelector((state: RootState) => state.auth.session?.user);
    const relationships = useSelector((state: RootState) => state.relationships.relationships);
    const notifications = useSelector((state: RootState) => state.notifications.notifications);
    const [refreshing, setRefreshing] = React.useState(false);

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        // TODO: Implement refresh logic
        setTimeout(() => setRefreshing(false), 1000);
    }, []);

    const handleCreateEvent = () => {
        // TODO: Navigate to create event
        console.log('Create event');
    };

    const handleViewEvents = () => {
        // TODO: Navigate to events
        console.log('View events');
    };

    const handleManageRelationships = () => {
        // TODO: Navigate to relationships
        console.log('Manage relationships');
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView
                style={styles.scrollView}
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                }
            >
                <View style={styles.header}>
                    <Text style={styles.greeting}>
                        Hello, {user?.user_metadata?.name || 'User'}!
                    </Text>
                    <Text style={styles.subtitle}>What would you like to do today?</Text>
                </View>

                <View style={styles.quickActions}>
                    <TouchableOpacity style={styles.actionCard} onPress={handleCreateEvent}>
                        <Ionicons name="add-circle" size={32} color="#4a90e2" />
                        <Text style={styles.actionTitle}>Create Event</Text>
                        <Text style={styles.actionDescription}>
                            Schedule a new event with friends
                        </Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.actionCard} onPress={handleViewEvents}>
                        <Ionicons name="calendar" size={32} color="#8e44ad" />
                        <Text style={styles.actionTitle}>View Events</Text>
                        <Text style={styles.actionDescription}>
                            See your upcoming events
                        </Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.actionCard} onPress={handleManageRelationships}>
                        <Ionicons name="people" size={32} color="#4a90e2" />
                        <Text style={styles.actionTitle}>Relationships</Text>
                        <Text style={styles.actionDescription}>
                            Manage your connections
                        </Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Recent Activity</Text>
                    {notifications.length > 0 ? (
                        <View style={styles.notificationsList}>
                            {notifications.slice(0, 3).map((notification) => (
                                <View key={notification.id} style={styles.notificationItem}>
                                    <Ionicons 
                                        name="notifications" 
                                        size={20} 
                                        color={notification.read ? "#525252" : "#4a90e2"} 
                                    />
                                    <View style={styles.notificationContent}>
                                        <Text style={styles.notificationTitle}>
                                            {notification.title}
                                        </Text>
                                        <Text style={styles.notificationMessage}>
                                            {notification.message}
                                        </Text>
                                    </View>
                                </View>
                            ))}
                        </View>
                    ) : (
                        <View style={styles.emptyState}>
                            <Ionicons name="notifications-outline" size={48} color="#d4d4d4" />
                            <Text style={styles.emptyStateText}>No recent activity</Text>
                        </View>
                    )}
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Your Relationships</Text>
                    {relationships.length > 0 ? (
                        <View style={styles.relationshipsList}>
                            {relationships.slice(0, 3).map((relationship) => (
                                <View key={relationship.id} style={styles.relationshipItem}>
                                    <Ionicons name="person" size={20} color="#4a90e2" />
                                    <Text style={styles.relationshipName}>
                                        {relationship.other_user.full_name}
                                    </Text>
                                </View>
                            ))}
                        </View>
                    ) : (
                        <View style={styles.emptyState}>
                            <Ionicons name="people-outline" size={48} color="#d4d4d4" />
                            <Text style={styles.emptyStateText}>No relationships yet</Text>
                        </View>
                    )}
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
    scrollView: {
        flex: 1,
    },
    header: {
        paddingHorizontal: 24,
        paddingVertical: 20,
    },
    greeting: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#262626',
        marginBottom: 4,
    },
    subtitle: {
        fontSize: 16,
        color: '#525252',
    },
    quickActions: {
        paddingHorizontal: 24,
        marginBottom: 32,
    },
    actionCard: {
        backgroundColor: 'white',
        padding: 20,
        borderRadius: 12,
        marginBottom: 12,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 3.84,
        elevation: 5,
    },
    actionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
        marginTop: 12,
        marginBottom: 4,
    },
    actionDescription: {
        fontSize: 14,
        color: '#525252',
        textAlign: 'center',
    },
    section: {
        paddingHorizontal: 24,
        marginBottom: 24,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
        marginBottom: 16,
    },
    notificationsList: {
        gap: 12,
    },
    notificationItem: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'white',
        padding: 16,
        borderRadius: 8,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 1,
        },
        shadowOpacity: 0.05,
        shadowRadius: 2,
        elevation: 2,
    },
    notificationContent: {
        flex: 1,
        marginLeft: 12,
    },
    notificationTitle: {
        fontSize: 14,
        fontWeight: '600',
        color: '#262626',
        marginBottom: 2,
    },
    notificationMessage: {
        fontSize: 12,
        color: '#525252',
    },
    relationshipsList: {
        gap: 12,
    },
    relationshipItem: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'white',
        padding: 16,
        borderRadius: 8,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 1,
        },
        shadowOpacity: 0.05,
        shadowRadius: 2,
        elevation: 2,
    },
    relationshipName: {
        fontSize: 14,
        color: '#262626',
        marginLeft: 12,
    },
    emptyState: {
        alignItems: 'center',
        paddingVertical: 32,
    },
    emptyStateText: {
        fontSize: 14,
        color: '#d4d4d4',
        marginTop: 8,
    },
});

export default HomeScreen;