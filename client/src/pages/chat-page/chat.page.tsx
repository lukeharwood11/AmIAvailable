import React, { useState, useRef, useEffect } from 'react';
import { LoadingIcon, Text } from '../../components';
import CollapsibleSidebar from '../../components/CollapsibleSidebar';
import styles from './chat.page.module.css';
import ChatMessage from './components/ChatMessage';
import { MessageInput, ChatHistory } from './components';
import { useSearchParams } from 'react-router';
import { useReduxAgent } from '../../hooks/useReduxAgent';
import { ChatMessage as AgentChatMessage } from '../../redux/types/agent.types';
import { SidebarAction } from '../../components/CollapsibleSidebar';
import { ChatHistoryItem } from './components/ChatHistory';
import { MdAdd } from 'react-icons/md';
import { useMediaQuery } from 'react-responsive';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'other';
  timestamp: Date;
}

const ChatPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [inputValue, setInputValue] = useState('');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(true);
  const isMobile = useMediaQuery({ query: '(max-width: 768px)' });
  useEffect(() => {
    setIsSidebarCollapsed(isMobile);
  }, [isMobile]);
  const [chatHistory, setChatHistory] = useState<ChatHistoryItem[]>([
    {
      id: '1',
      title: 'Meeting Planning',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      preview: 'Can you help me plan a team meeting for next week?',
    },
    {
      id: '2',
      title: 'Calendar Sync',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
      preview: 'I need to sync my calendar with my team members...',
    },
    {
      id: '3',
      title: 'Event Scheduling',
      timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
      preview: 'What are the best times to schedule a client call?',
    },
  ]);
  const [selectedHistoryId, setSelectedHistoryId] = useState<
    string | undefined
  >();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const hasProcessedInitialMessage = useRef(false);

  // Use Redux agent hook
  const {
    messages: agentMessages,
    isStreaming,
    loading,
    error,
    chatWithAmia,
    clearError,
  } = useReduxAgent();

  useEffect(() => {
    const message = searchParams.get('message');
    if (message && !hasProcessedInitialMessage.current) {
      hasProcessedInitialMessage.current = true;
      handleSendMessage(message);
      setSearchParams({});
    }
  }, [searchParams, setSearchParams]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // scroll to the bottom of the page
    scrollToBottom();
  }, [agentMessages]);

  useEffect(() => {
    // scroll to the top of the page
    window.scrollTo(0, 0);
  }, []);

  const handleSendMessage = async (input: string) => {
    if (input.trim()) {
      setInputValue('');
      clearError();
      try {
        const metadata = {};
        const context = {
          current_date: new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric',
            timeZone:
              Intl.DateTimeFormat().resolvedOptions().timeZone,
          }),
          current_time: new Date().toLocaleTimeString(),
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };

        await chatWithAmia(input.trim(), metadata, context);
        window.scrollTo(0, 0);
      } catch (err) {
        console.error('Failed to send message:', err);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  // Sidebar actions
  const sidebarActions: SidebarAction[] = [
    {
      id: 'new-chat',
      icon: <MdAdd size={16} />,
      label: 'New Chat',
      onClick: () => {
        setSelectedHistoryId(undefined);
        // Clear current messages by refreshing the page or calling a clear function
        window.location.reload();
      },
    },
  ];

  // History management functions
  const handleSelectHistory = (item: ChatHistoryItem) => {
    setSelectedHistoryId(item.id);
    // Here you would load the selected conversation
    // For now, we'll just show a placeholder
    console.log('Selected history item:', item);
  };

  const handleClearHistory = () => {
    setChatHistory([]);
    setSelectedHistoryId(undefined);
  };

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  return (
    <div
      className={`${styles.chatPage} ${isSidebarCollapsed ? styles.sidebarCollapsed : ''}`}
    >
      <CollapsibleSidebar
        isCollapsed={isSidebarCollapsed}
        onToggle={toggleSidebar}
        actions={sidebarActions}
      >
        <ChatHistory
          history={chatHistory}
          onSelectHistory={handleSelectHistory}
          onClearHistory={handleClearHistory}
          selectedItemId={selectedHistoryId}
        />
      </CollapsibleSidebar>

      <div
        className={`${styles.chatPageMainContent} ${isSidebarCollapsed ? styles.sidebarCollapsed : ''}`}
      >
        <div className={styles.chatHeader}></div>

        <div className={styles.messagesContainer}>
          <div className={styles.messagesList}>
            {agentMessages.map(
              (message: AgentChatMessage, index: number) => {
                const messageData: Message = {
                  id: `${message.role}-${index}`,
                  text: message.content,
                  sender:
                    message.role === 'user'
                      ? 'user'
                      : 'other',
                  timestamp: message.timestamp
                    ? new Date(message.timestamp)
                    : new Date(),
                };
                return (
                  <ChatMessage
                    key={messageData.id}
                    message={messageData}
                  />
                );
              }
            )}
            <div ref={messagesEndRef} />
            {(loading || isStreaming) &&
              (agentMessages[agentMessages.length - 1]?.role ===
                'user' ||
                (agentMessages[agentMessages.length - 1]
                  ?.role === 'assistant' &&
                  !agentMessages[
                    agentMessages.length - 1
                  ]?.content.trim())) && (
                <div className={styles.loadingContainer}>
                  <LoadingIcon size={30} />
                </div>
              )}
            {error && (
              <div className={styles.errorContainer}>
                <Text color='danger'>{error}</Text>
                <button onClick={clearError}>Dismiss</button>
              </div>
            )}
          </div>
        </div>

        <div className={styles.inputContainer}>
          <MessageInput
            placeholder={
              loading || isStreaming
                ? 'Amia is thinking...'
                : 'Ask me anything!'
            }
            value={inputValue}
            onChange={setInputValue}
            onSend={() => handleSendMessage(inputValue)}
            onKeyPress={handleKeyPress}
            disabled={loading || isStreaming}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
