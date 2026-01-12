# Quickstart Guide: Todo Application Backend

## Prerequisites

- Python 3.8 or higher
- PostgreSQL (local or cloud instance)
- Git
- pip (Python package installer)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
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
Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
ENVIRONMENT=development
LOG_LEVEL=info
```

Replace the database URL with your actual PostgreSQL connection string.

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

## Development Commands

### Running Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app
```

### Formatting Code
```bash
# Format code with black
black .

# Check for linting issues
flake8 .
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify that PostgreSQL is running
   - Check that the DATABASE_URL in `.env` is correct
   - Ensure the database exists and the user has proper permissions

2. **Module Import Errors**
   - Ensure the virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change the port in the uvicorn command: `uvicorn app.main:app --reload --port 8001`

### Checking Application Status
- Health check endpoint: `GET /health`
- API documentation: `GET /docs`
- Alternative API docs: `GET /redoc`

## Environment Configuration

### Development Environment
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_dev
LOG_LEVEL=debug
```

### Production Environment
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:password@prod-server:5432/todo_prod
LOG_LEVEL=warning
```

## Next Steps

1. Explore the API documentation at `/docs`
2. Test the endpoints using the interactive Swagger UI
3. Review the data models in the `app/models/` directory
4. Check the API routes in the `app/api/v1/` directory
5. Customize the application to meet your specific needs