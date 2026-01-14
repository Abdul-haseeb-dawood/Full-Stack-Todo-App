import { Task } from '@/models/task';

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

    return apiCall(`/api/v1/tasks${queryString}`);
  },

  // Get a specific task by ID
  getTaskById: async (id: string) => {
    return apiCall(`/api/v1/${id}`);
  },

  // Create a new task
  createTask: async (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => {
    // Ensure the completed field is included (defaults to false if not provided)
    const taskPayload = {
      ...taskData,
      completed: taskData.completed ?? false
    };

    return apiCall('/api/v1', {
      method: 'POST',
      body: JSON.stringify(taskPayload),
    });
  },

  // Update an existing task
  updateTask: async (id: string, taskData: Partial<Task>) => {
    return apiCall(`/api/v1/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Delete a task
  deleteTask: async (id: string) => {
    return apiCall(`/api/v1/${id}`, {
      method: 'DELETE',
    });
  },

  // Toggle task completion status (using the update endpoint)
  toggleTaskCompletion: async (id: string) => {
    // We'll fetch the task first to get its current state
    const task = await apiCall(`/api/v1/${id}`);
    // Then update just the completed status
    return apiCall(`/api/v1/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        completed: !task.completed
      }),
    });
  },
};

export default apiCall;