# Frontend Todo Application

This is a luxury-grade frontend todo application built with Next.js, TypeScript, and Tailwind CSS. It features stunning glassmorphic design, smooth micro-interactions, and full CRUD functionality integrated with a FastAPI backend.

## Features

- **Glassmorphic UI**: Beautiful glass-like cards with backdrop blur effects
- **Responsive Design**: Works on mobile, tablet, and desktop
- **CRUD Operations**: Create, read, update, and delete tasks
- **Search & Filter**: Find tasks by keyword, status, or priority
- **Sorting**: Sort tasks by due date, priority, or alphabetically
- **Language Toggle**: Switch between multiple languages instantly
- **Recurring Tasks**: Visual indicators for recurring tasks
- **Toast Notifications**: Success and error messages
- **Loading States**: Skeleton loaders during API calls

## Tech Stack

- Next.js 16+ with App Router
- TypeScript 5.0+
- Tailwind CSS for styling
- React 18+ with Context API for state management

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env.local` file in the frontend root directory:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_DEFAULT_LANGUAGE=en
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## API Integration

The application connects to a FastAPI backend at the configured API base URL. All API calls use the following endpoints:

- `GET /api/tasks` - Retrieve all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task details
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## Architecture

- `src/app/` - Next.js App Router pages
- `src/app/components/` - Reusable UI components
- `src/app/lib/` - Utility functions and API client
- `src/app/models/` - TypeScript interfaces
- `src/app/contexts/` - React context providers
- `src/app/public/` - Static assets
- `styles/` - Global styles

## Internationalization

The application supports multiple languages with instant switching. The language toggle button in the header allows users to switch between languages, and all text throughout the application updates instantly.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request