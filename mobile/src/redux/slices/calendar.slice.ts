import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { CalendarState, CalendarEvent, CalendarView } from '../../types';

const initialState: CalendarState = {
    events: [],
    loading: false,
    error: null,
    selectedDate: null,
    viewMode: 'month',
};

const calendarSlice = createSlice({
    name: 'calendar',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        setEvents: (state, action: PayloadAction<CalendarEvent[]>) => {
            state.events = action.payload;
            state.loading = false;
            state.error = null;
        },
        addEvent: (state, action: PayloadAction<CalendarEvent>) => {
            state.events.push(action.payload);
        },
        updateEvent: (state, action: PayloadAction<CalendarEvent>) => {
            const index = state.events.findIndex(e => e.id === action.payload.id);
            if (index !== -1) {
                state.events[index] = action.payload;
            }
        },
        removeEvent: (state, action: PayloadAction<string>) => {
            state.events = state.events.filter(e => e.id !== action.payload);
        },
        setSelectedDate: (state, action: PayloadAction<Date | null>) => {
            state.selectedDate = action.payload;
        },
        setViewMode: (state, action: PayloadAction<'month' | 'week' | 'day'>) => {
            state.viewMode = action.payload;
        },
        setView: (state, action: PayloadAction<CalendarView>) => {
            state.viewMode = action.payload.mode;
            state.selectedDate = action.payload.currentDate;
        },
    },
});

export const calendarActions = { ...calendarSlice.actions };

export default calendarSlice;