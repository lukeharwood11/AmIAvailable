import React, { useRef, useEffect, useState } from 'react';
import { Button } from '../../../components';
import { MdSend } from 'react-icons/md';
import styles from './MessageInput.module.css';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  onKeyPress: (e: React.KeyboardEvent) => void;
  placeholder?: string;
  disabled?: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({
  value,
  onChange,
  onSend,
  onKeyPress,
  placeholder = 'Type a message...',
  disabled = false,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isFocused, setIsFocused] = useState(false);

  const MIN_HEIGHT = 40;
  const MAX_HEIGHT = 120;

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const newHeight = Math.min(
        Math.max(textarea.scrollHeight, MIN_HEIGHT),
        MAX_HEIGHT
      );
      textarea.style.height = `${newHeight}px`;
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    } else {
      onKeyPress(e);
    }
  };

  const handleSend = () => {
    if (value.trim() && !disabled) {
      onSend();
      if (textareaRef && textareaRef.current) {
        console.log("I'm clicking the text area...")
        textareaRef.current.click();
      }
    }
  };

  return (
    <div
      className={`${styles.inputContainer} ${isFocused ? styles.focused : ''}`}
    >
      <div className={styles.inputWrapper}>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          disabled={disabled}
          className={styles.textarea}
          rows={1}
        />
        <Button
          onClick={handleSend}
          disabled={!value.trim() || disabled}
          variant='primary'
          size='small'
          className={styles.sendButton}
          rightIcon={<MdSend />}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default MessageInput;
