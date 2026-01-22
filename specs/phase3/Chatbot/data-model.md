# Data Model: Todo AI Chatbot UI

## Core Entities

### ChatMessage
Represents a single message in the conversation between user and AI assistant.

**Fields**:
- `id: string` - Unique identifier for the message
- `role: 'user' | 'assistant'` - Defines who sent the message
- `content: string` - The text content of the message
- `timestamp: Date` - When the message was created/sent
- `status: 'sent' | 'delivered' | 'error'` - Delivery status of the message
- `metadata?: object` - Optional additional data (e.g., for tool calls)

**Validation Rules**:
- `id` must be unique within the conversation
- `role` must be either 'user' or 'assistant'
- `content` must not be empty
- `timestamp` must be a valid date/time

### Conversation
Represents a collection of messages between the user and AI assistant.

**Fields**:
- `id: string` - Unique identifier for the conversation
- `title: string` - Display title for the conversation (auto-generated from first message or user-edited)
- `messages: ChatMessage[]` - Array of messages in chronological order
- `createdAt: Date` - When the conversation was started
- `updatedAt: Date` - When the conversation was last updated
- `isActive: boolean` - Whether this is the currently active conversation

**Validation Rules**:
- `id` must be unique
- `messages` must be sorted chronologically
- `createdAt` must be before or equal to `updatedAt`

### TodoAction
Represents an action extracted from user input that corresponds to a todo list operation.

**Fields**:
- `actionType: 'create' | 'update' | 'delete' | 'view' | 'search'` - Type of action to perform
- `targetId?: string` - ID of the target todo item (for update/delete)
- `parameters: object` - Action-specific parameters (e.g., title, description, priority for create)
- `extractedFrom: string` - Original user input that triggered this action

**Validation Rules**:
- `actionType` must be one of the defined values
- `targetId` is required for update/delete actions
- `parameters` must contain required fields based on action type

## State Management Models

### ChatState
Manages the state of the chat interface.

**Fields**:
- `currentConversation: Conversation` - The active conversation
- `isLoading: boolean` - Whether the AI is processing a response
- `inputValue: string` - Current value in the input field
- `error: string | null` - Any error messages to display
- `isConnected: boolean` - Connection status to the AI service

## UI Component Data Models

### MessageDisplayProps
Data structure for rendering messages in the UI.

**Fields**:
- `message: ChatMessage` - The message to display
- `isOwnMessage: boolean` - Whether this is the current user's message
- `showAvatar: boolean` - Whether to show sender avatar
- `onRetry?: () => void` - Handler for retrying failed messages

### InputAreaProps
Data structure for the chat input area.

**Fields**:
- `value: string` - Current input value
- `onChange: (value: string) => void` - Handler for input changes
- `onSend: (value: string) => void` - Handler for sending messages
- `disabled: boolean` - Whether the input is disabled
- `placeholder: string` - Placeholder text for the input