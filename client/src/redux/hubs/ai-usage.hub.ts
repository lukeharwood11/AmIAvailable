import axiosInstance from '../../lib/axios';
import { HTTP_METHODS, CONTENT_TYPES } from '../constants';
import { store } from '../store';
import { selectAccessToken } from '../selectors/auth.selectors';
import {
  AiUsageListResponse,
  AiUsageCostResponse,
  GetAiUsageRequest,
  GetAiUsageCostRequest,
} from '../types/ai-usage.types';

interface RequestConfig {
  method?: string;
  data?: any;
  params?: any;
  headers?: Record<string, string>;
}

// Helper function to make authenticated API requests
async function makeAuthenticatedRequest<T>(
  url: string,
  config: RequestConfig = {}
): Promise<T> {
  const { method = HTTP_METHODS.GET, data, params, headers = {} } = config;

  // Get current access token from Redux store
  const accessToken = selectAccessToken(store.getState());

  // Prepare headers
  const requestHeaders: Record<string, string> = {
    'Content-Type': CONTENT_TYPES.JSON,
    ...headers,
  };

  // Add authorization header if access token is available
  if (accessToken) {
    requestHeaders.Authorization = `Bearer ${accessToken}`;
  }

  // Make the request
  const response = await axiosInstance.request<T>({
    url,
    method,
    data,
    params,
    headers: requestHeaders,
  });

  return response.data;
}

// AI Usage API Functions
export const getAiUsage = async (
  request: GetAiUsageRequest = {}
): Promise<AiUsageListResponse> => {
  const { skip = 0, take = 10 } = request;

  return makeAuthenticatedRequest<AiUsageListResponse>('/api/v1/ai-usage', {
    method: HTTP_METHODS.GET,
    params: { skip, take },
  });
};

export const getAiUsageCost = async (
  request: GetAiUsageCostRequest
): Promise<AiUsageCostResponse> => {
  const { startDate, endDate } = request;

  return makeAuthenticatedRequest<AiUsageCostResponse>('/api/v1/ai-usage/cost', {
    method: HTTP_METHODS.GET,
    params: { startDate, endDate },
  });
};

export const getAiUsageByDateRange = async (
  request: GetAiUsageRequest & GetAiUsageCostRequest
): Promise<AiUsageListResponse> => {
  const { skip = 0, take = 10, startDate, endDate } = request;

  return makeAuthenticatedRequest<AiUsageListResponse>('/api/v1/ai-usage/by-date-range', {
    method: HTTP_METHODS.GET,
    params: { startDate, endDate, skip, take },
  });
};
