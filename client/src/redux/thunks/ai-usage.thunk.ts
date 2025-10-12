import { createAsyncThunk } from '@reduxjs/toolkit';
import { getAiUsage, getAiUsageCost, getAiUsageByDateRange } from '../hubs/ai-usage.hub';
import { aiUsageActions } from '../slices/ai-usage.slice';
import { GetAiUsageRequest, GetAiUsageCostRequest } from '../types/ai-usage.types';
import { ERROR_MESSAGES } from '../constants';

// Get AI usage records
export const fetchAiUsage = createAsyncThunk(
    'aiUsage/fetchAiUsage',
    async (request: GetAiUsageRequest = {}, { dispatch, rejectWithValue }) => {
        try {
            dispatch(aiUsageActions.setLoading(true));
            dispatch(aiUsageActions.clearError());

            const response = await getAiUsage(request);
            
            dispatch(aiUsageActions.setRecords({
                records: response.ai_usage_records,
                totalCount: response.total_count,
                skip: response.skip,
                take: response.take,
            }));

            return response;
        } catch (error) {
            const message = error instanceof Error 
                ? error.message 
                : ERROR_MESSAGES.GENERAL.REQUEST_FAILED;
            
            dispatch(aiUsageActions.setError(message));
            return rejectWithValue(message);
        } finally {
            dispatch(aiUsageActions.setLoading(false));
        }
    }
);

// Get AI usage cost
export const fetchAiUsageCost = createAsyncThunk(
    'aiUsage/fetchAiUsageCost',
    async (request: GetAiUsageCostRequest, { dispatch, rejectWithValue }) => {
        try {
            dispatch(aiUsageActions.setLoading(true));
            dispatch(aiUsageActions.clearError());

            const response = await getAiUsageCost(request);
            
            dispatch(aiUsageActions.setCostData(response));

            return response;
        } catch (error) {
            const message = error instanceof Error 
                ? error.message 
                : ERROR_MESSAGES.GENERAL.REQUEST_FAILED;
            
            dispatch(aiUsageActions.setError(message));
            return rejectWithValue(message);
        } finally {
            dispatch(aiUsageActions.setLoading(false));
        }
    }
);

// Get AI usage records by date range
export const fetchAiUsageByDateRange = createAsyncThunk(
    'aiUsage/fetchAiUsageByDateRange',
    async (request: GetAiUsageRequest & GetAiUsageCostRequest, { dispatch, rejectWithValue }) => {
        try {
            dispatch(aiUsageActions.setLoading(true));
            dispatch(aiUsageActions.clearError());

            const response = await getAiUsageByDateRange(request);
            
            dispatch(aiUsageActions.setRecords({
                records: response.ai_usage_records,
                totalCount: response.total_count,
                skip: response.skip,
                take: response.take,
            }));

            return response;
        } catch (error) {
            const message = error instanceof Error 
                ? error.message 
                : ERROR_MESSAGES.GENERAL.REQUEST_FAILED;
            
            dispatch(aiUsageActions.setError(message));
            return rejectWithValue(message);
        } finally {
            dispatch(aiUsageActions.setLoading(false));
        }
    }
);

// Refresh AI usage records (same as fetch but with current pagination)
export const refreshAiUsage = createAsyncThunk(
    'aiUsage/refreshAiUsage',
    async (_, { dispatch, getState, rejectWithValue }) => {
        try {
            const state = getState() as any;
            const { skip, take } = state.aiUsage;
            
            return dispatch(fetchAiUsage({ skip, take })).unwrap();
        } catch (error) {
            return rejectWithValue(error);
        }
    }
);