'use client';

import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { Task, TaskFilter, TaskSort, Toast, ModalState } from '@/models/task';
import { taskApi } from '@/lib/api';

// Define action types
type TaskAction =
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_FILTER'; payload: TaskFilter }
  | { type: 'SET_SORT'; payload: TaskSort }
  | { type: 'SET_MODAL'; payload: ModalState }
  | { type: 'SET_TOAST'; payload: Toast | null }
  | { type: 'CLEAR_TOAST' };

// Define state type
interface TaskState {
  tasks: Task[];
  filteredTasks: Task[];
  loading: boolean;
  error: string | null;
  filter: TaskFilter;
  sort: TaskSort;
  modal: ModalState;
  toast: Toast | null;
}

// Initial state
const initialState: TaskState = {
  tasks: [],
  filteredTasks: [],
  loading: false,
  error: null,
  filter: {},
  sort: 'due_date',
  modal: { isOpen: false, type: 'add' },
  toast: null,
};

// Reducer function
const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_TASKS':
      return {
        ...state,
        tasks: action.payload,
        filteredTasks: applyFiltersAndSort(action.payload, state.filter, state.sort),
        loading: false,
        error: null,
      };
    case 'ADD_TASK':
      const newTasksWithAdded = [...state.tasks, action.payload];
      return {
        ...state,
        tasks: newTasksWithAdded,
        filteredTasks: applyFiltersAndSort(newTasksWithAdded, state.filter, state.sort),
      };
    case 'UPDATE_TASK':
      const updatedTasks = state.tasks.map(task =>
        task.id === action.payload.id ? action.payload : task
      );
      return {
        ...state,
        tasks: updatedTasks,
        filteredTasks: applyFiltersAndSort(updatedTasks, state.filter, state.sort),
      };
    case 'DELETE_TASK':
      const remainingTasks = state.tasks.filter(task => task.id !== action.payload);
      return {
        ...state,
        tasks: remainingTasks,
        filteredTasks: applyFiltersAndSort(remainingTasks, state.filter, state.sort),
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'SET_FILTER':
      return {
        ...state,
        filter: action.payload,
        filteredTasks: applyFiltersAndSort(state.tasks, action.payload, state.sort),
      };
    case 'SET_SORT':
      return {
        ...state,
        sort: action.payload,
        filteredTasks: applyFiltersAndSort(state.tasks, state.filter, action.payload),
      };
    case 'SET_MODAL':
      return { ...state, modal: action.payload };
    case 'SET_TOAST':
      return { ...state, toast: action.payload };
    case 'CLEAR_TOAST':
      return { ...state, toast: null };
    default:
      return state;
  }
};

// Helper function to apply filters and sorting
const applyFiltersAndSort = (
  tasks: Task[],
  filter: TaskFilter,
  sort: TaskSort
): Task[] => {
  let filtered = tasks;

  // Apply status filter
  if (filter.status) {
    filtered = filtered.filter(task =>
      filter.status === 'completed' ? task.completed : !task.completed
    );
  }

  // Apply priority filter
  if (filter.priority) {
    filtered = filtered.filter(task => task.priority === filter.priority);
  }

  // Apply tag filter
  if (filter.tag) {
    filtered = filtered.filter(task => task.tags.includes(filter.tag!));
  }

  // Apply keyword search
  if (filter.keyword) {
    const keyword = filter.keyword.toLowerCase();
    filtered = filtered.filter(task =>
      task.title.toLowerCase().includes(keyword) ||
      (task.description && task.description.toLowerCase().includes(keyword))
    );
  }

  // Apply sorting
  switch (sort) {
    case 'due_date':
      filtered = [...filtered].sort((a, b) => {
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
      });
      break;
    case 'priority':
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      filtered = [...filtered].sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
      break;
    case 'alphabetical':
      filtered = [...filtered].sort((a, b) => a.title.localeCompare(b.title));
      break;
  }

  return filtered;
};

// Create context
const TaskContext = createContext<{
  state: TaskState;
  dispatch: React.Dispatch<TaskAction>;
  fetchTasks: () => Promise<void>;
  addTask: (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateTask: (id: string, taskData: Partial<Task>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<void>;
  openModal: (type: 'add' | 'edit', taskId?: string) => void;
  closeModal: () => void;
  showToast: (toast: Toast) => void;
  hideToast: () => void;
} | undefined>(undefined);

// Provider component
export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  // Fetch tasks from API
  const fetchTasks = React.useCallback(async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const response = await taskApi.getTasks();
      dispatch({ type: 'SET_TASKS', payload: response });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch tasks';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
    }
  }, []);

  // Add a new task
  const addTask = React.useCallback(async (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      const newTask = await taskApi.createTask(taskData);
      dispatch({ type: 'ADD_TASK', payload: newTask });
      showToast({
        id: Date.now().toString(),
        type: 'success',
        message: 'Task added successfully',
        duration: 3000,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to add task';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      showToast({
        id: Date.now().toString(),
        type: 'error',
        message: errorMessage,
        duration: 3000,
      });
    }
  }, []);

  // Update an existing task
  const updateTask = React.useCallback(async (id: string, taskData: Partial<Task>) => {
    try {
      const updatedTask = await taskApi.updateTask(id, taskData);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });
      showToast({
        id: Date.now().toString(),
        type: 'success',
        message: 'Task updated successfully',
        duration: 3000,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update task';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      showToast({
        id: Date.now().toString(),
        type: 'error',
        message: errorMessage,
        duration: 3000,
      });
    }
  }, []);

  // Delete a task
  const deleteTask = React.useCallback(async (id: string) => {
    try {
      await taskApi.deleteTask(id);
      dispatch({ type: 'DELETE_TASK', payload: id });
      showToast({
        id: Date.now().toString(),
        type: 'success',
        message: 'Task deleted successfully',
        duration: 3000,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete task';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      showToast({
        id: Date.now().toString(),
        type: 'error',
        message: errorMessage,
        duration: 3000,
      });
    }
  }, []);

  // Toggle task completion
  const toggleTaskCompletion = React.useCallback(async (id: string) => {
    try {
      const updatedTask = await taskApi.toggleTaskCompletion(id);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });
      showToast({
        id: Date.now().toString(),
        type: 'success',
        message: updatedTask.completed ? 'Task marked as complete' : 'Task marked as incomplete',
        duration: 3000,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update task completion';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      showToast({
        id: Date.now().toString(),
        type: 'error',
        message: errorMessage,
        duration: 3000,
      });
    }
  }, []);

  // Open modal
  const openModal = React.useCallback((type: 'add' | 'edit', taskId?: string) => {
    dispatch({
      type: 'SET_MODAL',
      payload: { isOpen: true, type, taskId },
    });
  }, []);

  // Close modal
  const closeModal = React.useCallback(() => {
    dispatch({
      type: 'SET_MODAL',
      payload: { isOpen: false, type: 'add' },
    });
  }, []);

  // Show toast notification
  const showToast = React.useCallback((toast: Toast) => {
    dispatch({ type: 'SET_TOAST', payload: toast });
    // Auto-hide toast after duration
    if (toast.duration !== 0) {
      setTimeout(() => {
        hideToast();
      }, toast.duration || 5000);
    }
  }, []);

  // Hide toast notification
  const hideToast = React.useCallback(() => {
    dispatch({ type: 'CLEAR_TOAST' });
  }, []);

  const value = {
    state,
    dispatch,
    fetchTasks,
    addTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    openModal,
    closeModal,
    showToast,
    hideToast,
  };

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
};

// Custom hook to use the task context
export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};