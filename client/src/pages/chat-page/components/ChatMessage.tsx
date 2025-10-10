import React, { useEffect, useState } from 'react';
import { Text } from '../../../components';
import styles from './ChatMessage.module.css';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    id: string;
    text: string;
    sender: 'user' | 'other';
    timestamp: Date;
}

interface ChatMessageProps {
    message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [isAnimating, setIsAnimating] = useState(false);

    useEffect(() => {
        // Trigger animation when component mounts
        const timer = setTimeout(() => {
            setIsVisible(true);
            setIsAnimating(true);
        }, 50);

        return () => clearTimeout(timer);
    }, []);

    const formatTime = (date: Date) => {
        return date.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const isUser = message.sender === 'user';

    return (
        <div
            className={`${styles.messageContainer} ${isUser ? styles.userMessage : styles.otherMessage}`}
        >
            <div
                className={`${styles.messageBubble} ${isUser ? styles.userBubble : styles.otherBubble} ${
                    isVisible ? styles.visible : ''
                } ${isAnimating ? styles.animating : ''}`}
            >
                <Text
                    variant='body'
                    className={isUser ? styles.userText : styles.otherText}
                >
                    {isUser ? (
                        message.text
                    ) : (
                        <Markdown remarkPlugins={[remarkGfm]}>
                            {message.text}
                        </Markdown>
                    )}
                </Text>
                <div
                    className={`${styles.timestamp} ${isUser ? styles.userTimestamp : styles.otherTimestamp}`}
                >
                    <Text variant='caption' className={styles.timestampText}>
                        {formatTime(message.timestamp)}
                    </Text>
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;
