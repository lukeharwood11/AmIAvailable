import { useCallback } from 'react';
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import {
    chatWithAmiaThunk,
    chatWithAmiaSyncThunk,
    clearConversationThunk,
} from '../redux/thunks/agent.thunk';
import { agentActions } from '../redux/slices/agent.slice';
import { ChatMessage } from '../redux/types/agent.types';

export function useReduxAgent() {
    const dispatch = useAppDispatch();
    const agent = useAppSelector(state => state.agent);

    // Chat with Amia using streaming
    const chatWithAmia = useCallback(
        async (
            message: string,
            metadata?: Record<string, any>,
            context?: Record<string, any>
        ) => {
            const messages: ChatMessage[] = [
                ...agent.messages,
                {
                    role: 'user',
                    content: message,
                    timestamp: new Date().toISOString(),
                },
            ];

            return dispatch(
                chatWithAmiaThunk({
                    messages,
                    metadata,
                    context,
                })
            );
        },
        [dispatch, agent.messages]
    );

    // Chat with Amia using sync (non-streaming)
    const chatWithAmiaSync = useCallback(
        async (
            message: string,
            metadata?: Record<string, any>,
            context?: Record<string, any>
        ) => {
            const messages: ChatMessage[] = [
                ...agent.messages,
                {
                    role: 'user',
                    content: message,
                    timestamp: new Date().toISOString(),
                },
            ];

            return dispatch(
                chatWithAmiaSyncThunk({
                    messages,
                    metadata,
                    context,
                })
            );
        },
        [dispatch, agent.messages]
    );

    // Clear conversation
    const clearConversation = useCallback(() => {
        return dispatch(clearConversationThunk());
    }, [dispatch]);

    // Add message manually
    const addMessage = useCallback(
        (message: ChatMessage) => {
            dispatch(agentActions.addMessage(message));
        },
        [dispatch]
    );

    // Clear error
    const clearError = useCallback(() => {
        dispatch(agentActions.clearError());
    }, [dispatch]);

    // Reset agent state
    const resetAgent = useCallback(() => {
        dispatch(agentActions.resetAgent());
    }, [dispatch]);

    return {
        // State
        messages: agent.messages,
        isStreaming: agent.isStreaming,
        loading: agent.loading,
        error: agent.error,

        // Actions
        chatWithAmia,
        chatWithAmiaSync,
        clearConversation,
        addMessage,
        clearError,
        resetAgent,
    };
}
