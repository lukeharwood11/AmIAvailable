import type { Meta, StoryObj } from '@storybook/react';
import Note from './Note';

const meta: Meta<typeof Note> = {
    title: 'Components/Note',
    component: Note,
    tags: ['autodocs'],
    argTypes: {
        variant: {
            control: 'select',
            options: ['error', 'warning', 'info', 'success'],
        },
        className: {
            control: 'text',
        },
        onClose: {
            action: 'closed',
        },
    },
};

export default meta;
type Story = StoryObj<typeof Note>;

// Icon components for stories
const ErrorIcon = () => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clipRule="evenodd"
        />
    </svg>
);

const WarningIcon = () => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path
            fillRule="evenodd"
            d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
            clipRule="evenodd"
        />
    </svg>
);

const InfoIcon = () => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path
            fillRule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
            clipRule="evenodd"
        />
    </svg>
);

const SuccessIcon = () => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clipRule="evenodd"
        />
    </svg>
);

export const Error: Story = {
    args: {
        variant: 'error',
        children: 'This is an error message',
    },
};

export const Warning: Story = {
    args: {
        variant: 'warning',
        children: 'This is a warning message',
    },
};

export const Info: Story = {
    args: {
        variant: 'info',
        children: 'This is an informational message',
    },
};

export const Success: Story = {
    args: {
        variant: 'success',
        children: 'Operation completed successfully!',
    },
};

export const ErrorWithIcon: Story = {
    args: {
        variant: 'error',
        children: 'An error occurred while processing your request',
        leftIcon: <ErrorIcon />,
    },
};

export const WarningWithIcon: Story = {
    args: {
        variant: 'warning',
        children: 'Please review your changes before continuing',
        leftIcon: <WarningIcon />,
    },
};

export const InfoWithIcon: Story = {
    args: {
        variant: 'info',
        children: 'This feature is currently in beta',
        leftIcon: <InfoIcon />,
    },
};

export const SuccessWithIcon: Story = {
    args: {
        variant: 'success',
        children: 'Your changes have been saved successfully',
        leftIcon: <SuccessIcon />,
    },
};

export const WithCloseButton: Story = {
    args: {
        variant: 'info',
        children: 'This note can be dismissed',
        onClose: () => console.log('Note closed'),
    },
};

export const ErrorWithClose: Story = {
    args: {
        variant: 'error',
        children: 'An error occurred. You can dismiss this message.',
        onClose: () => console.log('Error dismissed'),
    },
};

export const WithIconAndClose: Story = {
    args: {
        variant: 'warning',
        children: 'Your session will expire soon. Please save your work.',
        leftIcon: <WarningIcon />,
        onClose: () => console.log('Warning dismissed'),
    },
};

export const SuccessWithIconAndClose: Story = {
    args: {
        variant: 'success',
        children: 'File uploaded successfully!',
        leftIcon: <SuccessIcon />,
        onClose: () => console.log('Success dismissed'),
    },
};

export const LongMessage: Story = {
    args: {
        variant: 'warning',
        children:
            'This is a much longer warning message that demonstrates how the component handles extended text content. It might wrap to multiple lines depending on the container width.',
    },
};

export const LongMessageWithClose: Story = {
    args: {
        variant: 'success',
        children:
            'This is a much longer success message that demonstrates how the component handles extended text content with a close button. The close button should remain aligned at the top.',
        onClose: () => console.log('Success dismissed'),
    },
};

export const LongMessageWithIconAndClose: Story = {
    args: {
        variant: 'info',
        children:
            'This is a much longer informational message that demonstrates how the component handles extended text content with both an icon and a close button. The icon and close button should remain properly aligned with the text.',
        leftIcon: <InfoIcon />,
        onClose: () => console.log('Info dismissed'),
    },
};

export const ValidationError: Story = {
    args: {
        variant: 'error',
        children: 'Please enter a valid email address',
    },
};

export const NetworkError: Story = {
    args: {
        variant: 'error',
        children:
            'Unable to connect to server. Please check your internet connection and try again.',
        leftIcon: <ErrorIcon />,
        onClose: () => console.log('Network error dismissed'),
    },
};

export const WithCustomClass: Story = {
    args: {
        variant: 'info',
        children: 'Note with custom styling',
        className: 'custom-note-class',
    },
};

