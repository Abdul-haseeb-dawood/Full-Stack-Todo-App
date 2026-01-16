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
  // Get all tasks
  getTasks: async () => {
    return apiCall('/api/v1/tasks');
  },

  // Get a specific task by ID
  getTaskById: async (id: string) => {
    return apiCall(`/api/v1/tasks/${id}`);
  },

  // Create a new task
  createTask: async (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => {
    // Ensure the completed field is included (defaults to false if not provided)
    const taskPayload = {
      ...taskData,
      completed: taskData.completed ?? false
    };

    return apiCall('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(taskPayload),
    });
  },

  // Update an existing task
  updateTask: async (id: string, taskData: Partial<Task>) => {
    // Filter out undefined values and empty strings to prevent validation errors
    const filteredData = {};
    for (const [key, value] of Object.entries(taskData)) {
      // Only include values that are defined and not empty strings (for string fields)
      if (value !== undefined && !(typeof value === 'string' && value.trim() === '')) {
        filteredData[key] = value;
      }
    }

    return apiCall(`/api/v1/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(filteredData),
    });
  },

  // Delete a task
  deleteTask: async (id: string) => {
    const url = `${API_BASE_URL}/api/v1/tasks/${id}`;

    const config: RequestInit = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content response for delete
      if (response.status === 204) {
        return {}; // Return empty object for successful deletion
      }

      return await response.json();
    } catch (error) {
      console.error(`API call failed: ${url}`, error);
      throw error;
    }
  },

  // Toggle task completion status
  toggleTaskCompletion: async (id: string) => {
    return apiCall(`/api/v1/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  },
};

export default apiCall;