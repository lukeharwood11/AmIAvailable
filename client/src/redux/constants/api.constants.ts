// API Endpoints
export const API_ENDPOINTS = {
    RECIPES: '/api/v1/recipes',
    RECIPE_BY_ID: (id: number) => `/api/v1/recipes/${id}`,
    RECIPE_INGREDIENTS: (id: number) => `/api/v1/recipes/${id}/ingredients`,
    RECIPE_INGREDIENT_BY_ID: (id: number) =>
        `/api/v1/recipes/ingredients/${id}`,
    RECIPE_SEARCH: '/api/v1/recipes/search',

    // Calendar endpoints (if any)
    CALENDAR_EVENTS: '/api/v1/calendar/events',

    // Auth endpoints
    AUTH_TOKENS: '/api/v1/auth/tokens',

    // Agent endpoints
    AGENT_CHAT: '/api/v1/agent/commands/chat',

    // AI Usage endpoints
    AI_USAGE: '/api/v1/ai-usage',
    AI_USAGE_COST: '/api/v1/ai-usage/cost',
} as const;

// HTTP Methods
export const HTTP_METHODS = {
    GET: 'GET',
    POST: 'POST',
    PUT: 'PUT',
    DELETE: 'DELETE',
    PATCH: 'PATCH',
} as const;

// Request Headers
export const REQUEST_HEADERS = {
    CONTENT_TYPE: 'Content-Type',
    AUTHORIZATION: 'Authorization',
    ACCEPT: 'Accept',
} as const;

// Content Types
export const CONTENT_TYPES = {
    JSON: 'application/json',
    FORM_DATA: 'multipart/form-data',
    URL_ENCODED: 'application/x-www-form-urlencoded',
} as const;
