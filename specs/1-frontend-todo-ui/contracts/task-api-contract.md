# API Contracts: Frontend Todo UI

**Created**: 2026-01-06
**Feature**: 1-frontend-todo-ui

## Overview

This document defines the API contracts between the luxury frontend todo application and the FastAPI backend. These contracts ensure consistent data exchange and proper integration between the systems.

## Base API Configuration

### Base URL
```
https://api.example.com (production)
http://localhost:8000 (development)
```

### Common Headers
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token> (when implemented)
```

## Task Management Endpoints

### 1. Get All Tasks
- **Endpoint**: `GET /api/tasks`
- **Description**: Retrieve all tasks with optional filtering and sorting
- **Query Parameters**:
  - `status` (optional): `completed` | `incomplete`
  - `priority` (optional): `high` | `medium` | `low`
  - `due_date` (optional): ISO 8601 date string
  - `keyword` (optional): Search term for title/description
  - `sort` (optional): `due_date` | `priority` | `alphabetical`
  - `page` (optional): Page number for pagination
  - `limit` (optional): Number of items per page

- **Response**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Task description",
      "priority": "high",
      "tags": ["work", "important"],
      "completed": false,
      "due_date": "2026-12-31T23:59:59Z",
      "recurrence": "weekly",
      "created_at": "2026-01-01T10:00:00Z",
      "updated_at": "2026-01-01T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

- **Error Responses**:
  - `400 Bad Request`: Invalid query parameters
  - `500 Internal Server Error`: Server-side error

### 2. Create Task
- **Endpoint**: `POST /api/tasks`
- **Description**: Create a new task
- **Request Body**:
```json
{
  "title": "New task",
  "description": "Task description",
  "priority": "medium",
  "tags": ["work"],
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "daily"
}
```

- **Response**:
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "priority": "medium",
  "tags": ["work"],
  "completed": false,
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "daily",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z"
}
```

- **Validation**:
  - `title` is required and must be 1-200 characters
  - `priority` must be one of `high`, `medium`, `low`
  - `due_date` must be in ISO 8601 format if provided
  - `recurrence` must be one of `daily`, `weekly`, `monthly`, or null

- **Error Responses**:
  - `400 Bad Request`: Validation errors
  - `500 Internal Server Error`: Server-side error

### 3. Get Task by ID
- **Endpoint**: `GET /api/tasks/{id}`
- **Description**: Retrieve a specific task by ID
- **Path Parameter**: `id` - Task identifier
- **Response**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "priority": "high",
  "tags": ["work", "important"],
  "completed": false,
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "weekly",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z"
}
```

- **Error Responses**:
  - `404 Not Found`: Task with given ID does not exist
  - `500 Internal Server Error`: Server-side error

### 4. Update Task
- **Endpoint**: `PUT /api/tasks/{id}`
- **Description**: Update an existing task completely
- **Path Parameter**: `id` - Task identifier
- **Request Body**:
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "priority": "low",
  "tags": ["home"],
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "monthly"
}
```

- **Response**:
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "priority": "low",
  "tags": ["home"],
  "completed": false,
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "monthly",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-02T15:30:00Z"
}
```

- **Error Responses**:
  - `400 Bad Request`: Validation errors
  - `404 Not Found`: Task with given ID does not exist
  - `500 Internal Server Error`: Server-side error

### 5. Delete Task
- **Endpoint**: `DELETE /api/tasks/{id}`
- **Description**: Delete a specific task
- **Path Parameter**: `id` - Task identifier
- **Response**: `200 OK` with confirmation message
```json
{
  "message": "Task deleted successfully",
  "id": 1
}
```

- **Error Responses**:
  - `404 Not Found`: Task with given ID does not exist
  - `500 Internal Server Error`: Server-side error

### 6. Toggle Task Completion
- **Endpoint**: `PATCH /api/tasks/{id}/complete`
- **Description**: Toggle the completion status of a task
- **Path Parameter**: `id` - Task identifier
- **Request Body**: Empty
- **Response**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "priority": "high",
  "tags": ["work", "important"],
  "completed": true,
  "due_date": "2026-12-31T23:59:59Z",
  "recurrence": "weekly",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-02T16:00:00Z"
}
```

- **Error Responses**:
  - `404 Not Found`: Task with given ID does not exist
  - `500 Internal Server Error`: Server-side error

## Error Response Format

All error responses follow this format:
```json
{
  "error": "Error code or type",
  "message": "Human-readable error message",
  "details": { /* optional field with specific validation errors */ }
}
```

## Data Validation Rules

### Task Title
- Required field
- Minimum length: 1 character
- Maximum length: 200 characters

### Task Description
- Optional field
- Maximum length: 1000 characters

### Priority
- Required field
- Valid values: `high`, `medium`, `low`

### Tags
- Optional field
- Array of strings
- Each tag should be 1-50 characters

### Due Date
- Optional field
- Format: ISO 8601 datetime string
- Example: `2026-12-31T23:59:59Z`

### Recurrence
- Optional field
- Valid values: `daily`, `weekly`, `monthly`, `null`

## Authentication

For future implementation (Phase III):
- All endpoints require authentication via JWT token in Authorization header
- Token refresh mechanism to be implemented
- Session management for persistent login

## Rate Limiting

- API endpoints are rate-limited to 1000 requests per hour per IP
- Excessive requests return `429 Too Many Requests` response

## Versioning

- API versioning will be implemented via URL path: `/api/v1/tasks`
- Current version is v1 (version number omitted for initial release)
- Backward compatibility maintained for minor version updates