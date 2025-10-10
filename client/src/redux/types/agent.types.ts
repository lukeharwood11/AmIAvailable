// Agent State Types
export interface AgentState {
    messages: ChatMessage[];
    isStreaming: boolean;
    loading: boolean;
    error: string | null;
}

// Chat Message Types
export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

// API Request/Response Types
export interface ChatWithAmiaRequest {
    messages: ChatMessage[];
    metadata?: Record<string, any>;
    context?: Record<string, any>;
}

export interface ChatWithAmiaResponse {
    // This will be a streaming response, so we'll handle it differently
    content: string;
}
