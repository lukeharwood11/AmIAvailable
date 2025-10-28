import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RelationshipWithUserData, RequestState } from '../../types';

interface RelationshipsState {
    relationships: RelationshipWithUserData[];
    loading: boolean;
    error: string | null;
    createState: RequestState;
    updateState: RequestState;
    deleteState: RequestState;
}

const initialState: RelationshipsState = {
    relationships: [],
    loading: false,
    error: null,
    createState: { loading: false, error: null },
    updateState: { loading: false, error: null },
    deleteState: { loading: false, error: null },
};

const relationshipsSlice = createSlice({
    name: 'relationships',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        setRelationships: (state, action: PayloadAction<RelationshipWithUserData[]>) => {
            state.relationships = action.payload;
            state.loading = false;
            state.error = null;
        },
        addRelationship: (state, action: PayloadAction<RelationshipWithUserData>) => {
            state.relationships.push(action.payload);
        },
        updateRelationship: (state, action: PayloadAction<RelationshipWithUserData>) => {
            const index = state.relationships.findIndex(r => r.id === action.payload.id);
            if (index !== -1) {
                state.relationships[index] = action.payload;
            }
        },
        removeRelationship: (state, action: PayloadAction<string>) => {
            state.relationships = state.relationships.filter(r => r.id !== action.payload);
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

export const relationshipsActions = { ...relationshipsSlice.actions };

export default relationshipsSlice.reducer;