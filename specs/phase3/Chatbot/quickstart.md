# Quickstart Guide: Todo AI Chatbot UI

## Prerequisites

- Node.js 18+ installed
- Yarn or npm package manager
- Access to OpenAI API key (for ChatKit)
- Existing frontend project setup (Next.js, TypeScript, Tailwind CSS)

## Setup Instructions

### 1. Install Dependencies

First, install the required dependencies for the chatbot UI:

```bash
cd frontend
npm install @openai/chatkit-client
# OR if using yarn
yarn add @openai/chatkit-client
```

### 2. Environment Variables

Add the required environment variables to your `.env.local` file:

```env
NEXT_PUBLIC_CHATKIT_INSTANCE Locator=your-instance-locator
NEXT_PUBLIC_CHATKIT_KEY=your-key
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key
```

### 3. Create the Chat Route

Create the main chat page in `frontend/src/app/chat/page.tsx`:

```tsx
'use client';

import { useState, useEffect } from 'react';
import { ChatContainer } from './components/ChatContainer';
import { useChat } from '@/hooks/useChat';
import { ChatState } from '@/types/chat';

export default function ChatPage() {
  const [chatState, setChatState] = useState<ChatState>({
    currentConversation: {
      id: '',
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
    },
    isLoading: false,
    inputValue: '',
    error: null,
    isConnected: false,
  });

  const { sendMessage, connect, disconnect } = useChat(setChatState);

  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, []);

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm py-4 px-6">
        <h1 className="text-xl font-semibold text-gray-800">Todo AI Assistant</h1>
      </header>
      
      <main className="flex-1 overflow-hidden">
        <ChatContainer 
          chatState={chatState}
          onSendMessage={sendMessage}
        />
      </main>
    </div>
  );
}
```

### 4. Create the Chat Container Component

Create `frontend/src/app/chat/components/ChatContainer.tsx`:

```tsx
import { useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { WelcomeScreen } from './WelcomeScreen';
import { ChatState } from '@/types/chat';

interface ChatContainerProps {
  chatState: ChatState;
  onSendMessage: (message: string) => void;
}

export const ChatContainer = ({ chatState, onSendMessage }: ChatContainerProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatState.currentConversation.messages]);

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {chatState.currentConversation.messages.length === 0 ? (
        <WelcomeScreen onExamplePromptClick={onSendMessage} />
      ) : (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {chatState.currentConversation.messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              isOwnMessage={message.role === 'user'}
            />
          ))}
          {chatState.isLoading && (
            <MessageBubble
              message={{
                id: 'loading',
                role: 'assistant',
                content: 'Thinking...',
                timestamp: new Date(),
                status: 'sent'
              }}
              isOwnMessage={false}
            />
          )}
          <div ref={messagesEndRef} />
        </div>
      )}
      
      <div className="border-t border-gray-200 p-4 bg-white">
        <InputArea
          value={chatState.inputValue}
          onChange={(value) => 
            // Update chatState.inputValue - this would be handled by parent component
          }
          onSend={onSendMessage}
          disabled={chatState.isLoading}
        />
      </div>
    </div>
  );
};
```

### 5. Create the Message Bubble Component

Create `frontend/src/app/chat/components/MessageBubble.tsx`:

```tsx
import { ChatMessage } from '@/types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
  isOwnMessage: boolean;
}

export const MessageBubble = ({ message, isOwnMessage }: MessageBubbleProps) => {
  return (
    <div className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 ${
          isOwnMessage
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className={`text-xs mt-1 ${isOwnMessage ? 'text-blue-200' : 'text-gray-500'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};
```

### 6. Create the Input Area Component

Create `frontend/src/app/chat/components/InputArea.tsx`:

```tsx
import { useState, useRef, KeyboardEvent } from 'react';

interface InputAreaProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (value: string) => void;
  disabled: boolean;
}

export const InputArea = ({ value, onChange, onSend, disabled }: InputAreaProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (value.trim() && !disabled) {
      onSend(value);
      onChange('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
      
      // Update expanded state based on height
      setIsExpanded(textareaRef.current.scrollHeight > 100);
    }
  };

  // Adjust height when value changes
  if (textareaRef.current) {
    setTimeout(adjustTextareaHeight, 0);
  }

  return (
    <div className="relative">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Message Todo AI Assistant..."
        disabled={disabled}
        className={`w-full resize-none rounded-2xl border border-gray-300 px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
          isExpanded ? 'max-h-40' : 'max-h-20'
        }`}
      />
      <button
        onClick={handleSubmit}
        disabled={!value.trim() || disabled}
        className={`absolute right-3 bottom-3 rounded-full p-2 ${
          value.trim() && !disabled
            ? 'bg-blue-500 text-white hover:bg-blue-600'
            : 'bg-gray-200 text-gray-400 cursor-not-allowed'
        }`}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="h-5 w-5"
        >
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </div>
  );
};
```

### 7. Create the Welcome Screen Component

Create `frontend/src/app/chat/components/WelcomeScreen.tsx`:

```tsx
interface WelcomeScreenProps {
  onExamplePromptClick: (prompt: string) => void;
}

const EXAMPLE_PROMPTS = [
  'Add a task to buy groceries',
  'Show me my pending tasks',
  'Mark the presentation prep as complete',
  'Set the meeting notes task to high priority'
];

export const WelcomeScreen = ({ onExamplePromptClick }: WelcomeScreenProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-full p-4">
      <div className="text-center max-w-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Todo AI Assistant</h2>
        <p className="text-gray-600 mb-8">
          Interact with your todo list using natural language. Ask me to add, update, or find tasks.
        </p>
        
        <div className="space-y-3">
          <h3 className="font-medium text-gray-700">Try an example:</h3>
          {EXAMPLE_PROMPTS.map((prompt, index) => (
            <button
              key={index}
              onClick={() => onExamplePromptClick(prompt)}
              className="block w-full text-left p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors"
            >
              <span className="text-blue-600">→</span> {prompt}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
```

### 8. Create the Chat Hook

Create `frontend/src/hooks/useChat.ts`:

```tsx
import { useState, useCallback } from 'react';
import { ChatState } from '@/types/chat';

// Mock API client for initial implementation
const mockApiClient = {
  sendMessage: async (message: string, conversationId?: string) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Mock response based on message content
    let response = '';
    if (message.toLowerCase().includes('add') || message.toLowerCase().includes('create')) {
      response = `I've added "${message.replace(/add|create/i, '').trim()}" to your todo list.`;
    } else if (message.toLowerCase().includes('show') || message.toLowerCase().includes('list')) {
      response = "Here are your pending tasks: Buy groceries, Complete project proposal, Schedule team meeting.";
    } else {
      response = `I received your message: "${message}". How else can I help with your todos?`;
    }
    
    return {
      conversation_id: conversationId || `conv_${Date.now()}`,
      response,
      tool_calls: [],
      timestamp: new Date()
    };
  }
};

export const useChat = (setChatState: (state: ChatState) => void) => {
  const [isConnected, setIsConnected] = useState(false);

  const connect = useCallback(() => {
    // Initialize connection to chat service
    setIsConnected(true);
    console.log('Connected to chat service');
  }, []);

  const disconnect = useCallback(() => {
    // Cleanup connection to chat service
    setIsConnected(false);
    console.log('Disconnected from chat service');
  }, []);

  const sendMessage = useCallback(async (message: string) => {
    // Update UI to show loading state
    setChatState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      // Add user message to UI immediately
      const userMessage = {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        role: 'user' as const,
        content: message,
        timestamp: new Date(),
        status: 'sent' as const
      };

      setChatState(prev => ({
        ...prev,
        currentConversation: {
          ...prev.currentConversation,
          messages: [...prev.currentConversation.messages, userMessage],
          updatedAt: new Date()
        },
        inputValue: ''
      }));

      // Call API to get AI response
      const response = await mockApiClient.sendMessage(
        message,
        prev.currentConversation.id
      );

      // Add AI response to UI
      const aiMessage = {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        role: 'assistant' as const,
        content: response.response,
        timestamp: new Date(),
        status: 'sent' as const
      };

      setChatState(prev => ({
        ...prev,
        currentConversation: {
          ...prev.currentConversation,
          id: response.conversation_id,
          messages: [...prev.currentConversation.messages, aiMessage],
          updatedAt: new Date()
        },
        isLoading: false
      }));
    } catch (error) {
      console.error('Error sending message:', error);
      setChatState(prev => ({
        ...prev,
        error: 'Failed to send message. Please try again.',
        isLoading: false
      }));
    }
  }, [setChatState]);

  return {
    sendMessage,
    connect,
    disconnect,
    isConnected
  };
};
```

### 9. Create Type Definitions

Create `frontend/src/types/chat.ts`:

```tsx
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
  metadata?: object;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
}

export interface TodoAction {
  actionType: 'create' | 'update' | 'delete' | 'view' | 'search';
  targetId?: string;
  parameters: object;
  extractedFrom: string;
}

export interface ChatState {
  currentConversation: Conversation;
  isLoading: boolean;
  inputValue: string;
  error: string | null;
  isConnected: boolean;
}

export interface MessageDisplayProps {
  message: ChatMessage;
  isOwnMessage: boolean;
  showAvatar: boolean;
  onRetry?: () => void;
}

export interface InputAreaProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (value: string) => void;
  disabled: boolean;
}
```

### 10. Run the Application

After implementing all components, run the application:

```bash
cd frontend
npm run dev
# OR
yarn dev
```

Visit `http://localhost:3000/chat` to access the Todo AI Chatbot UI.

## Additional Configuration

### API Endpoint Configuration

The chat functionality connects to a backend API endpoint. For the initial implementation, this is mocked, but when the backend is ready, update the API endpoint in `frontend/src/lib/api/chatClient.ts`:

```ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;

export const sendChatMessage = async (message: string, conversationId?: string) => {
  // Implementation to call the real backend API
};
```

### Theming

The chat interface uses Tailwind CSS classes that follow the existing application theme. To customize the appearance, update the color classes in the components to match your design system.