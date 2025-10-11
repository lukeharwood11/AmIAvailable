import { useDispatch, useSelector } from 'react-redux';
import { useCallback } from 'react';
import { AppDispatch } from '../redux/store';
import {
  fetchAiUsage,
  fetchAiUsageCost,
  refreshAiUsage,
} from '../redux/thunks/ai-usage.thunk';
import {
  selectAiUsageRecords,
  selectAiUsageTotalCount,
  selectAiUsagePagination,
  selectAiUsageCostData,
  selectAiUsageLoading,
  selectAiUsageError,
  selectAiUsageHasRecords,
  selectAiUsageHasMoreRecords,
  selectAiUsageCurrentPage,
  selectAiUsageTotalPages,
  selectAiUsageTotalCost,
  selectAiUsageCostInRange,
} from '../redux/selectors/ai-usage.selectors';
import { GetAiUsageRequest, GetAiUsageCostRequest } from '../redux/types/ai-usage.types';

export const useReduxAiUsage = () => {
  const dispatch = useDispatch<AppDispatch>();

  // Selectors
  const records = useSelector(selectAiUsageRecords);
  const totalCount = useSelector(selectAiUsageTotalCount);
  const pagination = useSelector(selectAiUsagePagination);
  const costData = useSelector(selectAiUsageCostData);
  const loading = useSelector(selectAiUsageLoading);
  const error = useSelector(selectAiUsageError);
  const hasRecords = useSelector(selectAiUsageHasRecords);
  const hasMoreRecords = useSelector(selectAiUsageHasMoreRecords);
  const currentPage = useSelector(selectAiUsageCurrentPage);
  const totalPages = useSelector(selectAiUsageTotalPages);
  const totalCost = useSelector(selectAiUsageTotalCost);
  const costInRange = useSelector(selectAiUsageCostInRange);

  // Actions
  const loadAiUsage = useCallback(
    (request: GetAiUsageRequest = {}) => {
      return dispatch(fetchAiUsage(request));
    },
    [dispatch]
  );

  const loadAiUsageCost = useCallback(
    (request: GetAiUsageCostRequest) => {
      return dispatch(fetchAiUsageCost(request));
    },
    [dispatch]
  );

  const refresh = useCallback(() => {
    return dispatch(refreshAiUsage());
  }, [dispatch]);

  return {
    // State
    records,
    totalCount,
    pagination,
    costData,
    loading,
    error,
    hasRecords,
    hasMoreRecords,
    currentPage,
    totalPages,
    totalCost,
    costInRange,

    // Actions
    loadAiUsage,
    loadAiUsageCost,
    refresh,
  };
};
