// Task Model - The primary data structure representing a user's todo item
export interface Task {
  id: string; // UUID string
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  completed: boolean;
  due_date?: string; // ISO 8601 date string
  recurrence?: 'daily' | 'weekly' | 'monthly' | null;
  created_at: string; // ISO 8601 datetime string
  updated_at: string; // ISO 8601 datetime string
}

// UI State Models

// TaskFilter Model
export interface TaskFilter {
  status?: 'completed' | 'incomplete';
  priority?: 'high' | 'medium' | 'low';
  tag?: string;
  dueDate?: string; // ISO 8601 date string
  keyword?: string;
}

// TaskSort Model
export type TaskSort = 'due_date' | 'priority' | 'alphabetical';

// API Response Models

// Task List Response
export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  limit: number;
}

// API Error Response
export interface APIErrorResponse {
  error: string;
  message: string;
  code?: string;
}

// Component Data Models

// Toast Notification Model
export interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number; // milliseconds, default 5000
}

// Modal State Model
export interface ModalState {
  isOpen: boolean;
  type: 'add' | 'edit';
  taskId?: string; // for edit mode
}

// Form Data Models

// Task Form Model
export interface TaskFormData {
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  completed: boolean;
  due_date?: string;
  recurrence?: 'daily' | 'weekly' | 'monthly' | null;
}