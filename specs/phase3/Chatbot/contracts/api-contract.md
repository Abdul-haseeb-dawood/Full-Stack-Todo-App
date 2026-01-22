# API Contract: Todo AI Chatbot

## Overview
This document defines the API contract for the Todo AI Chatbot functionality. The API enables natural language interaction with the todo list through an AI assistant.

## Base URL
`/api/chat`

## Endpoints

### POST /api/chat
Initiates a conversation with the AI assistant or continues an existing conversation.

#### Request
```json
{
  "conversation_id": "string (optional)",
  "message": "string (required)",
  "user_id": "string (optional, mocked for now)"
}
```

#### Response
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": [
    {
      "type": "create_todo | update_todo | delete_todo | get_todos | search_todos",
      "params": {}
    }
  ],
  "timestamp": "ISO 8601 datetime string"
}
```

#### Example Request
```json
{
  "conversation_id": "conv_abc123",
  "message": "Add a task to buy groceries",
  "user_id": "user_123"
}
```

#### Example Response
```json
{
  "conversation_id": "conv_abc123",
  "response": "I've added 'buy groceries' to your todo list.",
  "tool_calls": [
    {
      "type": "create_todo",
      "params": {
        "title": "buy groceries",
        "priority": "medium"
      }
    }
  ],
  "timestamp": "2026-01-18T10:30:00Z"
}
```

### Error Responses
All endpoints return error responses in the following format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

#### Common Error Codes
- `INVALID_REQUEST`: Request body is malformed or missing required fields
- `CONVERSATION_NOT_FOUND`: Provided conversation_id does not exist
- `SERVICE_UNAVAILABLE`: AI service is temporarily unavailable
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same user

## Data Types

### Tool Call Object
Represents an action that the AI assistant wants to perform on the todo list.

```typescript
interface ToolCall {
  type: "create_todo" | "update_todo" | "delete_todo" | "get_todos" | "search_todos";
  params: object;
}
```

### Todo Object
Represents a todo item that may be returned as part of a tool call.

```typescript
interface Todo {
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
```

## Headers
- `Content-Type: application/json`
- `Authorization: Bearer {token}` (will be mocked for initial implementation)

## Rate Limiting
- 60 requests per minute per IP address
- 1000 requests per hour per authenticated user