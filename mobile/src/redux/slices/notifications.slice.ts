import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { NotificationData, NotificationState } from '../../types';

const initialState: NotificationState = {
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
};

const notificationsSlice = createSlice({
    name: 'notifications',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        setNotifications: (state, action: PayloadAction<NotificationData[]>) => {
            state.notifications = action.payload;
            state.unreadCount = action.payload.filter(n => !n.read).length;
            state.loading = false;
            state.error = null;
        },
        addNotification: (state, action: PayloadAction<NotificationData>) => {
            state.notifications.unshift(action.payload);
            if (!action.payload.read) {
                state.unreadCount += 1;
            }
        },
        updateNotification: (state, action: PayloadAction<NotificationData>) => {
            const index = state.notifications.findIndex(n => n.id === action.payload.id);
            if (index !== -1) {
                const wasUnread = !state.notifications[index].read;
                const isNowRead = action.payload.read;
                state.notifications[index] = action.payload;
                
                if (wasUnread && isNowRead) {
                    state.unreadCount -= 1;
                } else if (!wasUnread && !isNowRead) {
                    state.unreadCount += 1;
                }
            }
        },
        removeNotification: (state, action: PayloadAction<string>) => {
            const notification = state.notifications.find(n => n.id === action.payload);
            if (notification && !notification.read) {
                state.unreadCount -= 1;
            }
            state.notifications = state.notifications.filter(n => n.id !== action.payload);
        },
        markAsRead: (state, action: PayloadAction<string>) => {
            const notification = state.notifications.find(n => n.id === action.payload);
            if (notification && !notification.read) {
                notification.read = true;
                state.unreadCount -= 1;
            }
        },
        markAllAsRead: (state) => {
            state.notifications.forEach(notification => {
                if (!notification.read) {
                    notification.read = true;
                }
            });
            state.unreadCount = 0;
        },
    },
});

export const notificationsActions = { ...notificationsSlice.actions };

export default notificationsSlice.reducer;