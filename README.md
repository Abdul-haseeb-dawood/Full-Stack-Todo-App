# AI Task Management Chatbot

This is a full-stack AI task management application featuring an intelligent chatbot powered by Google's Gemini 1.5 Flash model with MCP-style tool calling capabilities.

## Features

- **AI-Powered Task Management**: Natural language interaction with an AI assistant to manage tasks
- **MCP-Style Tool Calling**: The AI can call various tools to perform actions like adding, reading, updating, completing, and deleting tasks
- **Real-Time Chat Interface**: Modern chat UI with conversation history
- **Persistent Storage**: Tasks and conversations stored in PostgreSQL database
- **Secure API Keys**: All sensitive information stored in environment variables

## Architecture

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Model**: Google Gemini 1.5 Flash
- **API**: RESTful endpoints with proper error handling

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS
- **UI Components**: Custom chat interface with ChatKit-style design

## MCP Tool Functions

The AI chatbot has access to the following tools:

1. **add_task**: Create a new task
   - Parameters: user_id, title, description (optional)

2. **read_task**: Read a specific task by ID
   - Parameters: user_id, task_id

3. **read_all_tasks**: Read all tasks with optional filters
   - Parameters: user_id, status (all/pending/completed), priority (low/medium/high)

4. **update_task**: Update task fields
   - Parameters: user_id, task_id, title (optional), description (optional), completed (optional), priority (optional)

5. **complete_task**: Mark a task as complete
   - Parameters: user_id, task_id

6. **delete_task**: Remove a task from the list
   - Parameters: user_id, task_id

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL database
- Google Gemini API key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Run the application:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your backend URL:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## Usage Examples

Once the application is running, you can interact with the AI assistant using natural language:

- "Add a task to buy groceries"
- "Show me my pending tasks"
- "Complete task 1"
- "Update task 2 to 'Call mom'"
- "Delete task 3"
- "Show high priority tasks"

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /api/chat/{user_id}`: Main chat endpoint for AI interactions

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL database connection string
- `GEMINI_API_KEY`: Google Gemini API key

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_BACKEND_URL`: Backend URL for API calls

## Deployment

### Backend
The backend can be deployed to any cloud platform that supports Python applications (Heroku, AWS, Google Cloud, etc.). Make sure to configure the environment variables appropriately.

### Frontend
The Next.js frontend can be deployed to Vercel, Netlify, or any hosting platform that supports Next.js applications.

## Error Handling

The application includes comprehensive error handling:
- API key validation
- Database connection errors
- Invalid user inputs
- Network timeouts
- Tool execution failures

## Security

- API keys are stored in environment variables and never exposed to the frontend
- User data is isolated by user_id
- Input validation and sanitization
- Proper authentication mechanisms (if needed for production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.