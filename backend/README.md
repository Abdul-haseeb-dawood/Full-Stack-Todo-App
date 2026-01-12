# Todo Application Backend

This is a production-ready backend for a Todo application with full CRUD functionality built using Python and FastAPI.

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon Cloud)
- **ORM**: SQLAlchemy (Async)
- **Migrations**: Alembic
- **Validation**: Pydantic
- **API Docs**: Swagger (FastAPI default)

## Project Structure

```
backend/
│── app/
│   │── main.py                 # FastAPI app instance
│   │── core/                   # Configuration settings
│   │   └── settings.py         # Settings management
│   │── db/                     # Database setup and session management
│   │   │── database.py         # Database engine and session
│   │   └── base.py             # Base model and mixins
│   │── models/                 # SQLAlchemy models
│   │   └── task.py             # Task model
│   │── schemas/                # Pydantic schemas
│   │   └── task.py             # Task schemas (create, update, response)
│   │── repositories/           # Data access layer
│   │   └── task_repository.py  # Task repository
│   │── services/               # Business logic
│   │   └── task_service.py     # Task service
│   │── routers/                # API routes
│   │   └── tasks.py            # Task-related routes
│   │── utils/                  # Utilities
│   │   └── exceptions.py       # Custom exceptions
│── .env                        # Environment variables
│── alembic.ini                 # Alembic configuration
│── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

On Linux/Mac:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Update the `.env` file with your actual PostgreSQL connection string:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
ENVIRONMENT=development
LOG_LEVEL=info
```

### 6. Set Up Database

Initialize the database with the required tables:

```bash
# Run database migrations
alembic upgrade head
```

### 7. Run the Application

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

API documentation will be available at `http://localhost:8000/docs`.

## API Endpoints

Once the application is running, you can access the following endpoints:

### Create a Task
- **Endpoint**: `POST /api/v1/tasks`
- **Request Body**:
```json
{
  "title": "Sample task",
  "description": "This is a sample task description",
  "completed": false
}
```

### Get All Tasks
- **Endpoint**: `GET /api/v1/tasks`

### Get a Specific Task
- **Endpoint**: `GET /api/v1/tasks/{task_id}`

### Update a Task
- **Endpoint**: `PUT /api/v1/tasks/{task_id}`
- **Request Body** (only include fields you want to update):
```json
{
  "title": "Updated task title",
  "completed": true
}
```

### Delete a Task
- **Endpoint**: `DELETE /api/v1/tasks/{task_id}`

## Key Design Choices

1. **UUID Primary Keys**: Using UUIDs for task IDs to ensure global uniqueness and prevent enumeration attacks.

2. **Async Operations**: All database operations use async/await patterns for better performance under load.

3. **Clean Architecture**: Clear separation of concerns between routers, services, repositories, models, and schemas.

4. **Proper Error Handling**: Custom exceptions and appropriate HTTP status codes for different error scenarios.

5. **Automatic Timestamps**: Created and updated timestamps are automatically managed by the database and ORM.

6. **CORS Configuration**: Properly configured to allow frontend integration without security restrictions.

7. **Validation**: Comprehensive validation at both API and model levels using Pydantic schemas.

## Database Schema

The application uses a single `tasks` table with the following structure:

- `id`: UUID (Primary Key, Unique, Not Null)
- `title`: String (Not Null, Max Length: 255)
- `description`: String (Optional, Max Length: 1000)
- `completed`: Boolean (Not Null, Default: False)
- `created_at`: DateTime (Not Null, Auto-generated)
- `updated_at`: DateTime (Not Null, Auto-generated, Updates on Change)

## Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Frontend Integration

The backend is designed for seamless integration with the frontend:

- CORS is configured to allow requests from any origin (adjust in production)
- JSON responses are consistent and predictable
- No authentication headers required
- All CRUD operations are fully supported
- Data persists across application restarts