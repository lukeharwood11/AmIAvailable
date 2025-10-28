// Calendar State Types
export interface CalendarState {
    events: CalendarEvent[];
    loading: boolean;
    error: string | null;
    selectedDate: Date | null;
    viewMode: 'month' | 'week' | 'day';
}

// Calendar Event Types
export interface CalendarEvent {
    id: string;
    title: string;
    description?: string;
    start: Date;
    end: Date;
    allDay: boolean;
    location?: string;
    attendees?: string[];
    status: 'confirmed' | 'tentative' | 'cancelled';
    created_by: string;
    created_at: string;
    updated_at: string;
}

// Calendar View Types
export interface CalendarView {
    mode: 'month' | 'week' | 'day';
    currentDate: Date;
}

// Calendar Filter Types
export interface CalendarFilters {
    status?: string[];
    attendees?: string[];
    dateRange?: {
        start: Date;
        end: Date;
    };
}