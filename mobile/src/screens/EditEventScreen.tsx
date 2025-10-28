import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    SafeAreaView,
    TextInput,
    Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const EditEventScreen = () => {
    // TODO: Get event from navigation params or Redux state
    const [title, setTitle] = useState('Sample Event');
    const [description, setDescription] = useState('This is a sample event description');
    const [location, setLocation] = useState('Sample Location');
    const [startDate, setStartDate] = useState('2024-01-15 10:00');
    const [endDate, setEndDate] = useState('2024-01-15 12:00');

    const handleSave = () => {
        if (!title.trim()) {
            Alert.alert('Error', 'Please enter a title for the event');
            return;
        }

        // TODO: Implement save event logic
        console.log('Updating event:', { title, description, location, startDate, endDate });
        Alert.alert('Success', 'Event updated successfully');
    };

    const handleCancel = () => {
        // TODO: Navigate back
        console.log('Cancel edit event');
    };

    const handleDelete = () => {
        Alert.alert(
            'Delete Event',
            'Are you sure you want to delete this event? This action cannot be undone.',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Delete',
                    style: 'destructive',
                    onPress: () => {
                        // TODO: Implement delete event logic
                        console.log('Deleting event');
                    },
                },
            ]
        );
    };

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={handleCancel}>
                    <Ionicons name="arrow-back" size={24} color="#4a90e2" />
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Edit Event</Text>
                <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
                    <Text style={styles.saveButtonText}>Save</Text>
                </TouchableOpacity>
            </View>

            <ScrollView style={styles.content}>
                <View style={styles.form}>
                    <View style={styles.inputGroup}>
                        <Text style={styles.inputLabel}>Event Title *</Text>
                        <TextInput
                            style={styles.input}
                            value={title}
                            onChangeText={setTitle}
                            placeholder="Enter event title"
                            placeholderTextColor="#d4d4d4"
                        />
                    </View>

                    <View style={styles.inputGroup}>
                        <Text style={styles.inputLabel}>Description</Text>
                        <TextInput
                            style={[styles.input, styles.textArea]}
                            value={description}
                            onChangeText={setDescription}
                            placeholder="Enter event description"
                            placeholderTextColor="#d4d4d4"
                            multiline
                            numberOfLines={4}
                        />
                    </View>

                    <View style={styles.inputGroup}>
                        <Text style={styles.inputLabel}>Location</Text>
                        <TextInput
                            style={styles.input}
                            value={location}
                            onChangeText={setLocation}
                            placeholder="Enter event location"
                            placeholderTextColor="#d4d4d4"
                        />
                    </View>

                    <View style={styles.inputGroup}>
                        <Text style={styles.inputLabel}>Start Date & Time</Text>
                        <TextInput
                            style={styles.input}
                            value={startDate}
                            onChangeText={setStartDate}
                            placeholder="YYYY-MM-DD HH:MM"
                            placeholderTextColor="#d4d4d4"
                        />
                    </View>

                    <View style={styles.inputGroup}>
                        <Text style={styles.inputLabel}>End Date & Time</Text>
                        <TextInput
                            style={styles.input}
                            value={endDate}
                            onChangeText={setEndDate}
                            placeholder="YYYY-MM-DD HH:MM"
                            placeholderTextColor="#d4d4d4"
                        />
                    </View>
                </View>

                <View style={styles.actions}>
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
    saveButton: {
        paddingHorizontal: 16,
        paddingVertical: 8,
    },
    saveButtonText: {
        color: '#4a90e2',
        fontSize: 16,
        fontWeight: '600',
    },
    content: {
        flex: 1,
        padding: 24,
    },
    form: {
        gap: 20,
        marginBottom: 32,
    },
    inputGroup: {
        gap: 8,
    },
    inputLabel: {
        fontSize: 14,
        fontWeight: '500',
        color: '#262626',
    },
    input: {
        backgroundColor: 'white',
        borderWidth: 1,
        borderColor: '#e5e5e5',
        borderRadius: 8,
        paddingHorizontal: 16,
        paddingVertical: 12,
        fontSize: 16,
        color: '#262626',
    },
    textArea: {
        height: 100,
        textAlignVertical: 'top',
    },
    actions: {
        gap: 12,
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

export default EditEventScreen;