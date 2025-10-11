import { createSelector } from '@reduxjs/toolkit';
import { RootState } from '../store';

// Base selectors
export const selectAiUsageState = (state: RootState) => state.aiUsage;

export const selectAiUsageRecords = createSelector(
    [selectAiUsageState],
    (aiUsage) => aiUsage.records
);

export const selectAiUsageTotalCount = createSelector(
    [selectAiUsageState],
    (aiUsage) => aiUsage.totalCount
);

export const selectAiUsagePagination = createSelector(
    [selectAiUsageState],
    (aiUsage) => ({
        skip: aiUsage.skip,
        take: aiUsage.take,
        totalCount: aiUsage.totalCount,
    })
);

export const selectAiUsageCostData = createSelector(
    [selectAiUsageState],
    (aiUsage) => aiUsage.costData
);

export const selectAiUsageLoading = createSelector(
    [selectAiUsageState],
    (aiUsage) => aiUsage.loading
);

export const selectAiUsageError = createSelector(
    [selectAiUsageState],
    (aiUsage) => aiUsage.error
);

// Computed selectors
export const selectAiUsageHasRecords = createSelector(
    [selectAiUsageRecords],
    (records) => records.length > 0
);

export const selectAiUsageHasMoreRecords = createSelector(
    [selectAiUsagePagination],
    ({ skip, take, totalCount }) => skip + take < totalCount
);

export const selectAiUsageCurrentPage = createSelector(
    [selectAiUsagePagination],
    ({ skip, take }) => Math.floor(skip / take) + 1
);

export const selectAiUsageTotalPages = createSelector(
    [selectAiUsagePagination],
    ({ take, totalCount }) => Math.ceil(totalCount / take)
);

export const selectAiUsageTotalCost = createSelector(
    [selectAiUsageRecords],
    (records) => records.reduce((total, record) => total + record.cost, 0)
);

export const selectAiUsageCostInRange = createSelector(
    [selectAiUsageCostData],
    (costData) => costData?.cost || 0
);

// Memoized selectors for specific records
export const selectAiUsageRecordById = (id: string) =>
    createSelector(
        [selectAiUsageRecords],
        (records) => records.find(record => record.id === id)
    );

export const selectAiUsageRecordsByDateRange = (startDate: string, endDate: string) =>
    createSelector(
        [selectAiUsageRecords],
        (records) => records.filter(record => {
            const recordDate = new Date(record.created_at);
            const start = new Date(startDate);
            const end = new Date(endDate);
            return recordDate >= start && recordDate <= end;
        })
    );