# Data Model: Frontend Todo UI

**Created**: 2026-01-06
**Feature**: 1-frontend-todo-ui

## Overview

This document defines the data structures and models used in the luxury frontend todo application. These models align with the backend API contracts and support the frontend's type safety requirements.

## Core Data Models

### Task Model

The primary data structure representing a user's todo item.

```ts
interface Task {
  id: number;
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
```

**Properties**:
- `id`: Unique identifier for the task
- `title`: Required short description of the task
- `description`: Optional detailed explanation of the task
- `priority`: Enum indicating task importance (high/medium/low)
- `tags`: Array of category labels (e.g., work, home)
- `completed`: Boolean indicating completion status
- `due_date`: Optional deadline for the task
- `recurrence`: Optional pattern for recurring tasks
- `created_at`: Timestamp when the task was created
- `updated_at`: Timestamp when the task was last modified

### UI State Models

#### TaskFilter Model
```ts
interface TaskFilter {
  status?: 'completed' | 'incomplete';
  priority?: 'high' | 'medium' | 'low';
  tag?: string;
  dueDate?: string; // ISO 8601 date string
  keyword?: string;
}
```

#### TaskSort Model
```ts
type TaskSort = 'due_date' | 'priority' | 'alphabetical';
```

#### Language Model
```ts
type Language = 'en' | 'es' | 'fr' | 'de' | 'ja' | 'zh'; // Extendable
```

## API Response Models

### Task List Response
```ts
interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  limit: number;
}
```

### API Error Response
```ts
interface APIErrorResponse {
  error: string;
  message: string;
  code?: string;
}
```

## Component Data Models

### Toast Notification Model
```ts
interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number; // milliseconds, default 5000
}
```

### Modal State Model
```ts
interface ModalState {
  isOpen: boolean;
  type: 'add' | 'edit';
  taskId?: number; // for edit mode
}
```

## Form Data Models

### Task Form Model
```ts
interface TaskFormData {
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  due_date?: string;
  recurrence?: 'daily' | 'weekly' | 'monthly' | null;
}
```

## Validation Models

### Task Validation Rules
```ts
interface TaskValidationRules {
  title: {
    required: true;
    minLength: 1;
    maxLength: 200;
  };
  description?: {
    maxLength: 1000;
  };
  due_date?: {
    format: 'ISO 8601';
  };
}
```

## Translation Models

### Translation Structure
```ts
interface Translation {
  [language: string]: {
    [key: string]: string;
  };
}
```

Example:
```ts
const translations: Translation = {
  en: {
    'app.title': 'Todo App',
    'task.add': 'Add Task',
    'task.edit': 'Edit Task'
  },
  es: {
    'app.title': 'Aplicación de Tareas',
    'task.add': 'Agregar Tarea',
    'task.edit': 'Editar Tarea'
  }
};
```

## Data Flow Patterns

### Task Creation Flow
1. User fills TaskFormData in modal
2. Form validation occurs using TaskValidationRules
3. Task object is created with additional metadata (id, timestamps)
4. Task is sent to backend API
5. On success, Task is added to frontend state

### Task Update Flow
1. Existing Task is loaded into TaskFormData
2. User modifies fields
3. Form validation occurs
4. Updated Task object is sent to backend API
5. On success, frontend state is updated

### Task Filtering Flow
1. User applies TaskFilter criteria
2. Frontend applies filters to local Task array
3. Results are displayed with smooth transitions

## Data Relationships

### Task to Tags
- One Task can have multiple Tags (many-to-many relationship)
- Tags are stored as string array within Task model
- Common tags: 'work', 'home', 'personal', 'urgent'

### Task to Priority
- Each Task has exactly one Priority value
- Priority values are constrained to 'high', 'medium', 'low'
- Priority affects visual styling and sorting

## Data Persistence

### Client-Side State
- Tasks are maintained in React state management
- Optimistic updates provide immediate UI feedback
- Error states trigger rollback of optimistic changes

### Server-Side Persistence
- Tasks stored in Neon PostgreSQL database
- Backend API provides CRUD operations
- Frontend communicates via REST endpoints