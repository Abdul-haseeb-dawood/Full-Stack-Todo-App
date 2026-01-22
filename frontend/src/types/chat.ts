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

export interface ToolCall {
  type: "create_todo" | "update_todo" | "delete_todo" | "get_todos" | "search_todos";
  params: object;
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  tags: string[];
  due_date?: string; // ISO 8601 date string
  created_at: string; // ISO 8601 datetime string
  updated_at: string; // ISO 8601 datetime string
}