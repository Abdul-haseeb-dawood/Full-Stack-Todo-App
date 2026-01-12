# Implementation Plan: Todo Application Backend

**Feature Branch**: `002-todo-backend-crud`
**Created**: 2026-01-11
**Status**: Draft

## Technical Context

This plan outlines the implementation of a complete backend for a Todo application with full CRUD functionality. The backend will be built using Python and FastAPI, with PostgreSQL (Neon Cloud) as the database and SQLAlchemy as the ORM.

### Technology Stack
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon Cloud)
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **API Documentation**: Swagger (FastAPI default)
- **Authentication**: Not required

### Key Decisions Made
- **ID Strategy**: Using UUIDs for task IDs to ensure global uniqueness
- **Async Operations**: Using async SQLAlchemy for better performance
- **RESTful Design**: Following standard REST conventions for API endpoints
- **CORS Configuration**: Allowing frontend integration without restrictions

## Constitution Check

This implementation follows the principles outlined in the project constitution:
- **Maintainability**: Clean separation of concerns with dedicated modules for routing, services, and data access
- **Scalability**: Async operations and proper connection pooling
- **Reliability**: Comprehensive error handling and validation
- **Security**: Input validation and proper error responses without exposing internal details

## Gates Evaluation

- **Architecture Gate**: PASSED - Clear separation of concerns with routers, services, repositories, models, and schemas
- **Integration Gate**: PASSED - Designed for seamless frontend integration with proper CORS and JSON responses
- **Quality Gate**: PASSED - Includes error handling, validation, and comprehensive API documentation

## Phase 0: Research & Unknowns Resolution

### Research Summary

#### Decision: ID Strategy
- **Rationale**: UUIDs provide global uniqueness without coordination, making them ideal for distributed systems and future scaling
- **Alternatives considered**: Auto-increment integers were considered but rejected due to potential issues with distributed systems and data merging

#### Decision: Async SQLAlchemy
- **Rationale**: Async operations allow better resource utilization and improved performance under load
- **Alternatives considered**: Synchronous SQLAlchemy was considered but async provides better scalability

#### Decision: RESTful API Design
- **Rationale**: Standard REST conventions provide predictability and compatibility with frontend frameworks
- **Alternatives considered**: GraphQL was considered but REST is simpler for this use case and well-supported by FastAPI

## Phase 1: Data Model & API Contracts

### Data Model: Task Entity

**Entity Name**: Task
- **id**: UUID (Primary Key, Unique, Not Null)
- **title**: String (Not Null, Max Length: 255)
- **description**: String (Optional, Max Length: 1000)
- **completed**: Boolean (Not Null, Default: False)
- **created_at**: DateTime (Not Null, Auto-generated)
- **updated_at**: DateTime (Not Null, Auto-generated, Updates on Change)

**Validation Rules**:
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- completed field must be a boolean value

**State Transitions**:
- New task: completed = False (default)
- Task completion: completed = True
- Task reopening: completed = False

### API Contract: Task Operations

#### POST /tasks - Create Task
- **Request Body**: 
  ```json
  {
    "title": "string (required, 1-255 chars)",
    "description": "string (optional, 0-1000 chars)",
    "completed": "boolean (optional, default: false)"
  }
  ```
- **Response**: 201 Created with created task object
- **Errors**: 400 Bad Request for validation errors

#### GET /tasks - List All Tasks
- **Query Parameters**: None
- **Response**: 200 OK with array of task objects
- **Errors**: 500 Internal Server Error for database issues

#### GET /tasks/{id} - Get Single Task
- **Path Parameter**: id (UUID format)
- **Response**: 200 OK with task object or 404 Not Found
- **Errors**: 404 Not Found if task doesn't exist

#### PUT /tasks/{id} - Update Task
- **Path Parameter**: id (UUID format)
- **Request Body**: Same as POST but all fields optional
- **Response**: 200 OK with updated task object or 404 Not Found
- **Errors**: 400 Bad Request for validation errors, 404 Not Found if task doesn't exist

#### DELETE /tasks/{id} - Delete Task
- **Path Parameter**: id (UUID format)
- **Response**: 204 No Content or 404 Not Found
- **Errors**: 404 Not Found if task doesn't exist

## Implementation Plan

### 1️⃣ Project Initialization Plan

#### 1.1 Virtual Environment Setup
- Create virtual environment: `python -m venv venv`
- Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- Upgrade pip: `pip install --upgrade pip`

#### 1.2 Dependency Selection and Reasoning
- **fastapi**: Modern, fast web framework with async support and automatic API documentation
- **uvicorn**: ASGI server for running the FastAPI application
- **sqlalchemy**: Powerful ORM with async support for database operations
- **asyncpg**: Async PostgreSQL driver for optimal performance
- **alembic**: Database migration management
- **pydantic**: Data validation and settings management
- **python-dotenv**: Environment variable management

#### 1.3 FastAPI App Bootstrap
- Create main application file: `main.py`
- Initialize FastAPI app with metadata
- Configure middleware (CORS, logging)
- Set up lifespan event handlers for startup/shutdown

#### 1.4 Environment Variable Management
- Create `.env` file with database connection details
- Use Pydantic's BaseSettings for configuration management
- Include Neon PostgreSQL connection string
- Add configuration for development vs production

#### 1.5 Neon PostgreSQL Connection Strategy
- Configure async SQLAlchemy engine with Neon connection string
- Implement connection pooling settings
- Handle SSL requirements for Neon Cloud

### 2️⃣ Database & ORM Planning

#### 2.1 PostgreSQL Schema Planning
- Design normalized schema for tasks table
- Define indexes for common query patterns
- Plan for future extensibility

#### 2.2 SQLAlchemy Async Engine/Session Setup
- Configure async engine with appropriate connection pool settings
- Create async session factory
- Implement proper connection lifecycle management

#### 2.3 Base Model Configuration
- Create declarative base class
- Implement common columns (created_at, updated_at) in base model
- Add helper methods for timestamp management

#### 2.4 Task Table Mapping
- Define Task model inheriting from base model
- Map all required fields (id, title, description, completed, timestamps)
- Add validation constraints at the model level

#### 2.5 Timestamp Handling
- Automatically set created_at on record creation
- Automatically update updated_at on record modification
- Use timezone-aware datetime objects

#### 2.6 UUID vs Integer ID Decision
- Use UUID primary keys for global uniqueness
- Implement proper UUID field handling in SQLAlchemy
- Ensure proper serialization for API responses

### 3️⃣ Migration Strategy

#### 3.1 Alembic Initialization
- Run `alembic init alembic` in project root
- Configure alembic.ini for async usage
- Set up migration directory structure

#### 3.2 Migration Workflow
- Generate initial migration for task table: `alembic revision --autogenerate -m "Initial task table"`
- Apply migrations: `alembic upgrade head`
- Create migration templates for common operations

#### 3.3 Schema Versioning
- Track schema changes with sequential migration files
- Maintain backward compatibility where possible
- Document breaking changes in migration files

#### 3.4 Safe Upgrade/Downgrade Strategy
- Implement proper downgrade operations for all migrations
- Test migration reversibility
- Handle data migration if needed

### 4️⃣ Application Architecture Plan

#### 4.1 Folder & Module Breakdown
```
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
│   │       └── tasks.py        # Task-related routes
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

#### 4.2 Responsibilities of Each Layer

##### Routers
- Handle HTTP request/response cycle
- Validate path/query parameters
- Call service layer methods
- Format responses according to API contract

##### Services
- Implement business logic
- Coordinate between models and repositories
- Handle complex operations involving multiple entities
- Manage transactions where needed

##### Repositories (Data Access Layer)
- Direct database operations
- Abstract SQL queries
- Handle CRUD operations for specific entities
- Manage connections and sessions

##### Models
- Define database schema through ORM
- Include validation rules
- Implement relationships between entities
- Provide helper methods for common operations

##### Schemas
- Define request/response data structures
- Handle data validation with Pydantic
- Convert between API representations and internal models
- Manage serialization/deserialization

##### Database Config
- Initialize database connections
- Configure engines and sessions
- Handle connection pooling
- Manage lifecycle events

#### 4.3 Dependency Injection Flow
- Use FastAPI's built-in dependency injection
- Inject database sessions into route handlers
- Share configuration across components
- Implement reusable dependencies for common operations

### 5️⃣ CRUD API Planning

#### 5.1 Create Task Operation
- **Route**: `POST /api/v1/tasks`
- **Request Flow**: 
  1. Validate request body against TaskCreate schema
  2. Call task service create method
  3. Service creates new Task model instance
  4. Repository saves to database
  5. Return created task with 201 status
- **Validation Logic**: Title required (1-255 chars), description optional (0-1000 chars)
- **Business Rules**: Set completed to False by default
- **DB Interaction**: Insert new record with auto-generated timestamps
- **Response Structure**: Return full task object with generated ID and timestamps
- **Status Codes**: 201 Created on success, 400 Bad Request on validation error

#### 5.2 Read Task Operations
- **Route**: `GET /api/v1/tasks` (list) and `GET /api/v1/tasks/{id}` (single)
- **Request Flow**:
  1. Validate path parameter for single task endpoint
  2. Call task service get methods
  3. Repository fetches from database
  4. Return task(s) in response
- **Validation Logic**: Validate UUID format for single task lookup
- **Business Rules**: Return tasks in descending order of creation date
- **DB Interaction**: SELECT queries with appropriate filtering
- **Response Structure**: Array for list, single object for individual task
- **Status Codes**: 200 OK for success, 404 Not Found for missing task

#### 5.3 Update Task Operation
- **Route**: `PUT /api/v1/tasks/{id}`
- **Request Flow**:
  1. Validate path parameter and request body
  2. Verify task exists
  3. Update task with provided fields
  4. Save changes to database
  5. Return updated task
- **Validation Logic**: Validate UUID format and request body fields
- **Business Rules**: Only update provided fields, preserve others
- **DB Interaction**: UPDATE query with optimistic locking if needed
- **Response Structure**: Return updated task object
- **Status Codes**: 200 OK for success, 404 Not Found if task doesn't exist, 400 for validation errors

#### 5.4 Delete Task Operation
- **Route**: `DELETE /api/v1/tasks/{id}`
- **Request Flow**:
  1. Validate path parameter
  2. Verify task exists
  3. Delete task from database
  4. Return success response
- **Validation Logic**: Validate UUID format
- **Business Rules**: Soft delete or hard delete decision
- **DB Interaction**: DELETE query
- **Response Structure**: Empty response body
- **Status Codes**: 204 No Content for success, 404 Not Found if task doesn't exist

### 6️⃣ Error Handling & Validation Plan

#### 6.1 Custom Exceptions
- Define application-specific exception classes
- Create base `TodoException` class
- Implement specific exceptions: `TaskNotFoundException`, `ValidationError`

#### 6.2 HTTP Error Handling
- **404 Not Found**: When requested task doesn't exist
- **400 Bad Request**: When request data fails validation
- **500 Internal Server Error**: For unexpected server errors
- **422 Unprocessable Entity**: For validation errors from Pydantic

#### 6.3 Database Failure Handling
- Catch database-specific exceptions
- Log database errors appropriately
- Return user-friendly error messages
- Implement retry logic for transient failures

#### 6.4 Validation Errors via Pydantic
- Leverage Pydantic's automatic validation
- Customize error messages for better UX
- Handle nested object validation
- Validate at both schema and model levels

### 7️⃣ Swagger & API Documentation Plan

#### 7.1 Auto-generated Docs Strategy
- Leverage FastAPI's automatic OpenAPI/Swagger generation
- Use Pydantic models for request/response schemas
- Add descriptive docstrings for endpoints
- Include example requests and responses

#### 7.2 Endpoint Naming Conventions
- Use RESTful URL patterns: `/api/v1/tasks`
- Consistent naming across all endpoints
- Clear, descriptive operation IDs
- Group related operations logically

#### 7.3 Example Request/Response Models
- Provide realistic examples in API documentation
- Include sample data that demonstrates API usage
- Show both success and error response examples
- Document all possible status codes

#### 7.4 Developer Experience Focus
- Enable interactive API testing in Swagger UI
- Provide clear parameter descriptions
- Include links to related documentation
- Make API exploration intuitive

### 8️⃣ Frontend Integration Plan

#### 8.1 CORS Configuration
- Configure CORS middleware to allow frontend domain
- Support credentials if needed in future
- Allow standard HTTP methods (GET, POST, PUT, DELETE)
- Permit necessary headers for API communication

#### 8.2 API Base URL Strategy
- Use configurable base URL for different environments
- Support both development and production endpoints
- Implement proper URL construction in frontend
- Handle API versioning in URLs

#### 8.3 JSON Response Standardization
- Consistent response format across all endpoints
- Proper serialization of datetime objects
- Standardized error response format
- Include necessary metadata in responses

#### 8.4 Handling Refresh & Persistence
- Ensure data persists across application restarts
- Verify database connections survive restarts
- Test data integrity after deployment
- Implement proper cleanup on shutdown

#### 8.5 Avoiding Breaking Changes
- Maintain API compatibility during development
- Use versioning for major changes
- Document any changes that affect frontend
- Coordinate with frontend team on API evolution

### 9️⃣ Performance & Best Practices

#### 9.1 Async DB Access
- Use async SQLAlchemy methods throughout
- Implement proper async/await patterns
- Avoid blocking operations in request handlers
- Monitor for sync/async mismatches

#### 9.2 Connection Pooling
- Configure appropriate pool sizes for expected load
- Set connection timeouts appropriately
- Monitor connection usage in production
- Handle pool exhaustion gracefully

#### 9.3 Avoiding N+1 Queries
- Use eager loading where appropriate
- Implement proper relationship handling
- Profile queries during development
- Use SQLAlchemy's query optimization techniques

#### 9.4 Clean Shutdown/Startup Events
- Implement startup event to initialize database connections
- Implement shutdown event to close connections properly
- Handle graceful shutdown signals
- Ensure data consistency during shutdown

### 🔟 Development & Testing Workflow

#### 🔟.1 Local Development Flow
- Use development settings with local database
- Implement hot-reloading for faster development
- Use uvicorn with reload option
- Maintain separate configurations for dev/prod

#### 🔟.2 Manual Testing via Swagger
- Test all endpoints through Swagger UI
- Verify request/response formats
- Test error conditions manually
- Validate data validation rules

#### 🔟.3 DB Verification Steps
- Manually inspect database after operations
- Verify data integrity and constraints
- Check timestamp updates work correctly
- Validate foreign key relationships if added

#### 🔟.4 Debugging Strategy
- Implement structured logging
- Use debug endpoints for development
- Log important operations and errors
- Include correlation IDs for request tracing
