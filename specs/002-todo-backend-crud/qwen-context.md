# Qwen Agent Context: Todo Application Backend

## Project Overview
This project implements a complete backend for a Todo application with full CRUD functionality using Python and FastAPI, with PostgreSQL (Neon Cloud) as the database and SQLAlchemy as the ORM.

## Technology Stack
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon Cloud)
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **API Documentation**: Swagger (FastAPI default)
- **Dependencies**: 
  - fastapi
  - uvicorn
  - sqlalchemy (async)
  - asyncpg
  - alembic
  - pydantic
  - python-dotenv

## Architecture
- **Separation of Concerns**: Clear division between routers, services, repositories, models, and schemas
- **Async Operations**: Using async SQLAlchemy for better performance
- **RESTful Design**: Following standard REST conventions for API endpoints
- **UUID Strategy**: Using UUIDs for task IDs to ensure global uniqueness

## Key Implementation Details

### Data Model: Task Entity
- **id**: UUID (Primary Key, Unique, Not Null)
- **title**: String (Not Null, Max Length: 255)
- **description**: String (Optional, Max Length: 1000)
- **completed**: Boolean (Not Null, Default: False)
- **created_at**: DateTime (Not Null, Auto-generated)
- **updated_at**: DateTime (Not Null, Auto-generated, Updates on Change)

### API Endpoints
- **POST /api/v1/tasks**: Create a new task
- **GET /api/v1/tasks**: List all tasks
- **GET /api/v1/tasks/{id}**: Get a specific task
- **PUT /api/v1/tasks/{id}**: Update a task
- **DELETE /api/v1/tasks/{id}**: Delete a task

### Validation Rules
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- completed field must be a boolean value

### Error Handling
- 404 Not Found: When requested task doesn't exist
- 400 Bad Request: When request data fails validation
- 500 Internal Server Error: For unexpected server errors
- 422 Unprocessable Entity: For validation errors from Pydantic

## File Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI app instance
│   ├── config/
│   │   └── settings.py         # Configuration settings
│   ├── database/
│   │   ├── base.py             # Base model and engine setup
│   │   └── session.py          # Session management
│   ├── models/
│   │   └── task.py             # Task model
│   ├── schemas/
│   │   ├── task.py             # Task schemas (create, update, response)
│   │   └── common.py           # Shared schemas
│   ├── api/
│   │   └── v1/
│   │       └── tasks.py        # Task-related routes
│   └── services/
│       └── task_service.py     # Task business logic
├── alembic/                    # Migration files
├── requirements.txt            # Dependencies
└── .env                        # Environment variables
```

## Development Workflow
- Use virtual environment for dependency isolation
- Apply database migrations with Alembic
- Test endpoints via Swagger UI
- Follow async/await patterns throughout
- Implement proper error handling and validation

## Environment Configuration
- Use .env file for environment-specific settings
- Separate configurations for development and production
- Secure database connection strings
- Configure CORS for frontend integration