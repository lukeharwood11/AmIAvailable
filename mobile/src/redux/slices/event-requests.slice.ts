import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { EventRequestWithUserData, RequestState } from '../../types';

interface EventRequestsState {
    eventRequests: EventRequestWithUserData[];
    loading: boolean;
    error: string | null;
    createState: RequestState;
    updateState: RequestState;
    deleteState: RequestState;
}

const initialState: EventRequestsState = {
    eventRequests: [],
    loading: false,
    error: null,
    createState: { loading: false, error: null },
    updateState: { loading: false, error: null },
    deleteState: { loading: false, error: null },
};

const eventRequestsSlice = createSlice({
    name: 'eventRequests',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        setEventRequests: (state, action: PayloadAction<EventRequestWithUserData[]>) => {
            state.eventRequests = action.payload;
            state.loading = false;
            state.error = null;
        },
        addEventRequest: (state, action: PayloadAction<EventRequestWithUserData>) => {
            state.eventRequests.push(action.payload);
        },
        updateEventRequest: (state, action: PayloadAction<EventRequestWithUserData>) => {
            const index = state.eventRequests.findIndex(r => r.id === action.payload.id);
            if (index !== -1) {
                state.eventRequests[index] = action.payload;
            }
        },
        removeEventRequest: (state, action: PayloadAction<string>) => {
            state.eventRequests = state.eventRequests.filter(r => r.id !== action.payload);
        },
        setCreateState: (state, action: PayloadAction<RequestState>) => {
            state.createState = action.payload;
        },
        setUpdateState: (state, action: PayloadAction<RequestState>) => {
            state.updateState = action.payload;
        },
        setDeleteState: (state, action: PayloadAction<RequestState>) => {
            state.deleteState = action.payload;
        },
    },
});

export const eventRequestsActions = { ...eventRequestsSlice.actions };

export default eventRequestsSlice.reducer;