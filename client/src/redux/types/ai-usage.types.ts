
// AI Usage Data Types
export interface AiUsageData {
  id: string;
  user_id: string;
  cost: number;
  usage: Record<string, any>;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// AI Usage Response Types
export interface AiUsageResponse {
  status: string;
  ai_usage: AiUsageData;
  message?: string;
}

export interface AiUsageListResponse {
  status: string;
  ai_usage_records: AiUsageData[];
  total_count: number;
  skip: number;
  take: number;
}

export interface AiUsageCostResponse {
  start_date: string;
  end_date: string;
  cost: number;
}

// AI Usage State Types
export interface AiUsageState {
  records: AiUsageData[];
  totalCount: number;
  skip: number;
  take: number;
  costData: AiUsageCostResponse | null;
  loading: boolean;
  error: string | null;
}

// Request Types
export interface GetAiUsageRequest {
  skip?: number;
  take?: number;
}

export interface GetAiUsageCostRequest {
  startDate: string;
  endDate: string;
}
