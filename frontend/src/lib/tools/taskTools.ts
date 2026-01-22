import { Task } from '@/types/task';

// Define the shape of our tool responses
export interface ToolResult {
  success: boolean;
  message: string;
  data?: any;
}

// Define the shape of our tool calls
export interface ToolCall {
  type: string;
  params: Record<string, any>;
}

/**
 * Tool to add a new task
 */
export const addTaskTool = async (params: { title: string; description?: string; priority?: 'low' | 'medium' | 'high'; dueDate?: string }): Promise<ToolResult> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: params.title,
        description: params.description || '',
        priority: params.priority || 'medium',
        due_date: params.dueDate || null,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to add task');
    }

    const newTask: Task = await response.json();

    return {
      success: true,
      message: `Successfully added task: "${newTask.title}"`,
      data: newTask
    };
  } catch (error) {
    return {
      success: false,
      message: `Error adding task: ${(error as Error).message}`
    };
  }
};

/**
 * Tool to update an existing task
 */
export const updateTaskTool = async (params: { id: string; title?: string; description?: string; status?: 'pending' | 'in-progress' | 'completed'; priority?: 'low' | 'medium' | 'high'; dueDate?: string }): Promise<ToolResult> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/${params.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...(params.title !== undefined && { title: params.title }),
        ...(params.description !== undefined && { description: params.description }),
        ...(params.status !== undefined && { status: params.status }),
        ...(params.priority !== undefined && { priority: params.priority }),
        ...(params.dueDate !== undefined && { due_date: params.dueDate }),
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to update task');
    }

    const updatedTask: Task = await response.json();

    return {
      success: true,
      message: `Successfully updated task: "${updatedTask.title}"`,
      data: updatedTask
    };
  } catch (error) {
    return {
      success: false,
      message: `Error updating task: ${(error as Error).message}`
    };
  }
};

/**
 * Tool to delete a task
 */
export const deleteTaskTool = async (params: { id: string }): Promise<ToolResult> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/${params.id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to delete task');
    }

    return {
      success: true,
      message: 'Successfully deleted task'
    };
  } catch (error) {
    return {
      success: false,
      message: `Error deleting task: ${(error as Error).message}`
    };
  }
};

/**
 * Tool to get all tasks
 */
export const getTasksTool = async (): Promise<ToolResult> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch tasks');
    }

    const tasks: Task[] = await response.json();

    return {
      success: true,
      message: `Retrieved ${tasks.length} tasks`,
      data: tasks
    };
  } catch (error) {
    return {
      success: false,
      message: `Error fetching tasks: ${(error as Error).message}`
    };
  }
};

/**
 * Tool to get tasks by status
 */
export const getTasksByStatusTool = async (params: { status: 'pending' | 'in-progress' | 'completed' }): Promise<ToolResult> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/?status=${params.status}`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch tasks');
    }

    const tasks: Task[] = await response.json();

    return {
      success: true,
      message: `Retrieved ${tasks.length} ${params.status} tasks`,
      data: tasks
    };
  } catch (error) {
    return {
      success: false,
      message: `Error fetching tasks: ${(error as Error).message}`
    };
  }
};

/**
 * Tool to mark a task as complete
 */
export const markTaskCompleteTool = async (params: { id: string }): Promise<ToolResult> => {
  return updateTaskTool({ id: params.id, status: 'completed' });
};

/**
 * Tool to set task priority
 */
export const setTaskPriorityTool = async (params: { id: string; priority: 'low' | 'medium' | 'high' }): Promise<ToolResult> => {
  return updateTaskTool({ id: params.id, priority: params.priority });
};

// Map of available tools
export const availableTools: Record<string, (params: any) => Promise<ToolResult>> = {
  'add_task': addTaskTool,
  'update_task': updateTaskTool,
  'delete_task': deleteTaskTool,
  'get_tasks': getTasksTool,
  'get_tasks_by_status': getTasksByStatusTool,
  'mark_task_complete': markTaskCompleteTool,
  'set_task_priority': setTaskPriorityTool,
};