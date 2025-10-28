import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    FlatList,
    TouchableOpacity,
    SafeAreaView,
    RefreshControl,
} from 'react-native';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { Ionicons } from '@expo/vector-icons';

interface Event {
    id: string;
    title: string;
    description?: string;
    start: Date;
    end: Date;
    location?: string;
    status: 'confirmed' | 'tentative' | 'cancelled';
}

const EventsScreen = () => {
    const events = useSelector((state: RootState) => state.calendar.events);
    const [refreshing, setRefreshing] = useState(false);

    const onRefresh = () => {
        setRefreshing(true);
        // TODO: Implement refresh logic
        setTimeout(() => setRefreshing(false), 1000);
    };

    const handleCreateEvent = () => {
        // TODO: Navigate to create event
        console.log('Create event');
    };

    const handleEventPress = (event: Event) => {
        // TODO: Navigate to event detail
        console.log('Event pressed:', event.id);
    };

    const renderEvent = ({ item }: { item: Event }) => (
        <TouchableOpacity
            style={styles.eventCard}
            onPress={() => handleEventPress(item)}
        >
            <View style={styles.eventHeader}>
                <Text style={styles.eventTitle}>{item.title}</Text>
                <View style={[styles.statusBadge, styles[`status${item.status}`]]}>
                    <Text style={styles.statusText}>{item.status}</Text>
                </View>
            </View>
            
            {item.description && (
                <Text style={styles.eventDescription}>{item.description}</Text>
            )}
            
            <View style={styles.eventDetails}>
                <View style={styles.eventDetail}>
                    <Ionicons name="time" size={16} color="#525252" />
                    <Text style={styles.eventDetailText}>
                        {item.start.toLocaleDateString()} at {item.start.toLocaleTimeString()}
                    </Text>
                </View>
                
                {item.location && (
                    <View style={styles.eventDetail}>
                        <Ionicons name="location" size={16} color="#525252" />
                        <Text style={styles.eventDetailText}>{item.location}</Text>
                    </View>
                )}
            </View>
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Events</Text>
                <TouchableOpacity style={styles.createButton} onPress={handleCreateEvent}>
                    <Ionicons name="add" size={24} color="white" />
                </TouchableOpacity>
            </View>

            {events.length > 0 ? (
                <FlatList
                    data={events}
                    renderItem={renderEvent}
                    keyExtractor={(item) => item.id}
                    contentContainerStyle={styles.listContainer}
                    refreshControl={
                        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                    }
                />
            ) : (
                <View style={styles.emptyState}>
                    <Ionicons name="calendar-outline" size={64} color="#d4d4d4" />
                    <Text style={styles.emptyTitle}>No events yet</Text>
                    <Text style={styles.emptyDescription}>
                        Create your first event to get started
                    </Text>
                    <TouchableOpacity style={styles.emptyButton} onPress={handleCreateEvent}>
                        <Text style={styles.emptyButtonText}>Create Event</Text>
                    </TouchableOpacity>
                </View>
            )}
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
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingVertical: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#e5e5e5',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#262626',
    },
    createButton: {
        backgroundColor: '#4a90e2',
        width: 40,
        height: 40,
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    listContainer: {
        padding: 24,
        gap: 16,
    },
    eventCard: {
        backgroundColor: 'white',
        padding: 16,
        borderRadius: 12,
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
        marginBottom: 8,
    },
    eventTitle: {
        fontSize: 16,
        fontWeight: '600',
        color: '#262626',
        flex: 1,
    },
    statusBadge: {
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 12,
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
        fontWeight: '500',
        color: '#262626',
    },
    eventDescription: {
        fontSize: 14,
        color: '#525252',
        marginBottom: 12,
    },
    eventDetails: {
        gap: 8,
    },
    eventDetail: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    eventDetailText: {
        fontSize: 14,
        color: '#525252',
    },
    emptyState: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 24,
    },
    emptyTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#262626',
        marginTop: 16,
        marginBottom: 8,
    },
    emptyDescription: {
        fontSize: 14,
        color: '#525252',
        textAlign: 'center',
        marginBottom: 24,
    },
    emptyButton: {
        backgroundColor: '#4a90e2',
        paddingHorizontal: 24,
        paddingVertical: 12,
        borderRadius: 8,
    },
    emptyButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
});

export default EventsScreen;