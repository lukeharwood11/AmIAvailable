import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const EventDetailScreen = () => {
    // TODO: Get event from navigation params or Redux state
    const event = {
        id: '1',
        title: 'Sample Event',
        description: 'This is a sample event description',
        start: new Date(),
        end: new Date(Date.now() + 2 * 60 * 60 * 1000), // 2 hours later
        location: 'Sample Location',
        status: 'confirmed' as const,
    };

    const handleEdit = () => {
        // TODO: Navigate to edit event
        console.log('Edit event');
    };

    const handleDelete = () => {
        // TODO: Implement delete event
        console.log('Delete event');
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="#4a90e2" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Event Details</Text>
                <TouchableOpacity style={styles.menuButton}>
                    <Ionicons name="ellipsis-vertical" size={24} color="#4a90e2" />
                </TouchableOpacity>
            </View>

            <ScrollView style={styles.content}>
                <View style={styles.eventCard}>
                    <View style={styles.eventHeader}>
                        <Text style={styles.eventTitle}>{event.title}</Text>
                        <View style={[styles.statusBadge, styles[`status${event.status}`]]}>
                            <Text style={styles.statusText}>{event.status}</Text>
                        </View>
                    </View>

                    {event.description && (
                        <Text style={styles.eventDescription}>{event.description}</Text>
                    )}

                    <View style={styles.eventDetails}>
                        <View style={styles.eventDetail}>
                            <Ionicons name="time" size={20} color="#4a90e2" />
                            <View style={styles.eventDetailContent}>
                                <Text style={styles.eventDetailLabel}>Start Time</Text>
                                <Text style={styles.eventDetailValue}>
                                    {event.start.toLocaleDateString()} at {event.start.toLocaleTimeString()}
                                </Text>
                            </View>
                        </View>

                        <View style={styles.eventDetail}>
                            <Ionicons name="time" size={20} color="#8e44ad" />
                            <View style={styles.eventDetailContent}>
                                <Text style={styles.eventDetailLabel}>End Time</Text>
                                <Text style={styles.eventDetailValue}>
                                    {event.end.toLocaleDateString()} at {event.end.toLocaleTimeString()}
                                </Text>
                            </View>
                        </View>

                        {event.location && (
                            <View style={styles.eventDetail}>
                                <Ionicons name="location" size={20} color="#4a90e2" />
                                <View style={styles.eventDetailContent}>
                                    <Text style={styles.eventDetailLabel}>Location</Text>
                                    <Text style={styles.eventDetailValue}>{event.location}</Text>
                                </View>
                            </View>
                        )}
                    </View>
                </View>

                <View style={styles.actions}>
                    <TouchableOpacity style={styles.editButton} onPress={handleEdit}>
                        <Ionicons name="create" size={20} color="white" />
                        <Text style={styles.editButtonText}>Edit Event</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
                        <Ionicons name="trash" size={20} color="#ff6b6b" />
                        <Text style={styles.deleteButtonText}>Delete Event</Text>
                    </TouchableOpacity>
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
    backButton: {
        padding: 8,
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
    },
    menuButton: {
        padding: 8,
    },
    content: {
        flex: 1,
        padding: 24,
    },
    eventCard: {
        backgroundColor: 'white',
        padding: 20,
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
    eventHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12,
    },
    eventTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#262626',
        flex: 1,
    },
    statusBadge: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 16,
    },
    statusconfirmed: {
        backgroundColor: '#d4edda',
    },
    statustentative: {
        backgroundColor: '#fff3cd',
    },
    statuscancelled: {
        backgroundColor: '#f8d7da',
    },
    statusText: {
        fontSize: 12,
        fontWeight: '600',
        color: '#262626',
    },
    eventDescription: {
        fontSize: 16,
        color: '#525252',
        lineHeight: 24,
        marginBottom: 20,
    },
    eventDetails: {
        gap: 16,
    },
    eventDetail: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12,
    },
    eventDetailContent: {
        flex: 1,
    },
    eventDetailLabel: {
        fontSize: 12,
        fontWeight: '500',
        color: '#525252',
        marginBottom: 2,
    },
    eventDetailValue: {
        fontSize: 14,
        color: '#262626',
    },
    actions: {
        gap: 12,
    },
    editButton: {
        backgroundColor: '#4a90e2',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 16,
        paddingHorizontal: 24,
        borderRadius: 8,
        gap: 8,
    },
    editButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
    deleteButton: {
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
    deleteButtonText: {
        color: '#ff6b6b',
        fontSize: 16,
        fontWeight: '600',
    },
});

export default EventDetailScreen;