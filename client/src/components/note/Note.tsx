import React from 'react';
import styles from './Note.module.css';

export type NoteVariant = 'error' | 'warning' | 'info' | 'success';

interface NoteProps {
    children: React.ReactNode;
    className?: string;
    variant?: NoteVariant;
    onClose?: () => void;
    leftIcon?: React.ReactNode;
}

const Note: React.FC<NoteProps> = ({ 
    children, 
    className, 
    variant = 'info',
    onClose,
    leftIcon
}) => {
    const noteClasses = [
        styles.note,
        styles[variant],
        className
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <div className={noteClasses}>
            {leftIcon && (
                <span className={styles.leftIcon}>{leftIcon}</span>
            )}
            <div className={styles.content}>{children}</div>
            {onClose && (
                <button 
                    className={styles.closeButton}
                    onClick={onClose}
                    aria-label="Close"
                    type="button"
                >
                    ×
                </button>
            )}
        </div>
    );
};

export default Note;

