import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AiUsageState, AiUsageData, AiUsageCostResponse } from '../types/ai-usage.types';

const initialState: AiUsageState = {
    records: [],
    totalCount: 0,
    skip: 0,
    take: 10,
    costData: null,
    loading: false,
    error: null,
};

const aiUsageSlice = createSlice({
    name: 'aiUsage',
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload;
        },
        setRecords: (state, action: PayloadAction<{
            records: AiUsageData[];
            totalCount: number;
            skip: number;
            take: number;
        }>) => {
            const { records, totalCount, skip, take } = action.payload;
            state.records = records;
            state.totalCount = totalCount;
            state.skip = skip;
            state.take = take;
        },
        setCostData: (state, action: PayloadAction<AiUsageCostResponse | null>) => {
            state.costData = action.payload;
        },
        clearRecords: (state) => {
            state.records = [];
            state.totalCount = 0;
            state.skip = 0;
            state.take = 10;
        },
        clearCostData: (state) => {
            state.costData = null;
        },
        clearError: (state) => {
            state.error = null;
        },
        reset: () => initialState,
    },
});

export const aiUsageActions = aiUsageSlice.actions;
export const aiUsageReducer = aiUsageSlice.reducer;