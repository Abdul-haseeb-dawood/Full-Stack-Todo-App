# spec Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-11

## Active Technologies

- Python + FastAPI (002-todo-backend-crud)
- PostgreSQL (002-todo-backend-crud)
- SQLAlchemy (002-todo-backend-crud)

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance
│   ├── config/                 # Configuration settings
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/               # Database setup and session management
│   │   ├── __init__.py
│   │   ├── base.py             # Base model and engine setup
│   │   └── session.py          # Session management
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── task.py             # Task model
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── task.py             # Task schemas (create, update, response)
│   │   └── common.py           # Shared schemas
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   └── v1/                 # Version 1 API routes
│   │       ├── __init__.py
│       └── tasks.py            # Task-related routes
│   └── services/               # Business logic
│       ├── __init__.py
│       └── task_service.py     # Task business logic
├── alembic/                    # Migration files
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └──.ini
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
└── .gitignore                  # Git ignore file
```

## Commands

cd backend; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Code Style

Python: Follow standard conventions with async/await patterns for database operations, proper error handling, and separation of concerns between routers, services, repositories, models, and schemas.

## Recent Changes

- 002-todo-backend-crud: Added Python + FastAPI
- 002-todo-backend-crud: Added PostgreSQL
- 002-todo-backend-crud: Added SQLAlchemy

<!-- MANUAL ADDITIONS START -->
<!-- For the Todo Application Backend feature, focus on the following key points:

1. Architecture: Emphasize the separation of concerns between routers, services, repositories, models, and schemas
2. Async Operations: Use async/await patterns throughout for optimal performance
3. Database: Implement proper async SQLAlchemy patterns with Neon PostgreSQL
4. API Design: Follow RESTful conventions with proper HTTP status codes
5. Validation: Use Pydantic for request/response validation
6. Error Handling: Implement proper error responses with appropriate HTTP status codes
7. UUID Strategy: Use UUIDs for task IDs to ensure global uniqueness
8. Timestamps: Automatically manage created_at and updated_at timestamps
9. Migrations: Use Alembic for database schema management
10. CORS: Configure properly for frontend integration
-->
<!-- MANUAL ADDITIONS END -->