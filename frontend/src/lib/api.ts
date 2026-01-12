import { Task } from '@/src/models/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Generic API call function with error handling
const apiCall = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API call failed: ${url}`, error);
    throw error;
  }
};

// Task API functions
export const taskApi = {
  // Get all tasks with optional filters
  getTasks: async (filters?: {
    status?: 'completed' | 'incomplete';
    priority?: 'high' | 'medium' | 'low';
    dueDate?: string;
    keyword?: string;
    sort?: 'due_date' | 'priority' | 'alphabetical';
  }) => {
    let queryString = '';
    if (filters) {
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.priority) params.append('priority', filters.priority);
      if (filters.dueDate) params.append('due_date', filters.dueDate);
      if (filters.keyword) params.append('keyword', filters.keyword);
      if (filters.sort) params.append('sort', filters.sort);
      queryString = `?${params.toString()}`;
    }
    
    return apiCall(`/api/tasks${queryString}`);
  },

  // Get a specific task by ID
  getTaskById: async (id: number) => {
    return apiCall(`/api/tasks/${id}`);
  },

  // Create a new task
  createTask: async (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => {
    return apiCall('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  // Update an existing task
  updateTask: async (id: number, taskData: Partial<Task>) => {
    return apiCall(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Delete a task
  deleteTask: async (id: number) => {
    return apiCall(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  },

  // Toggle task completion status
  toggleTaskCompletion: async (id: number) => {
    return apiCall(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  },
};

export default apiCall;