# Quickstart Guide: Frontend Todo UI

## Overview

This quickstart guide provides instructions for setting up, running, and testing the luxury frontend todo application. The application features stunning glassmorphic design, smooth micro-interactions, and full CRUD functionality integrated with a FastAPI backend.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the FastAPI backend server
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend root directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_DEFAULT_LANGUAGE=en
```

### 4. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Features Walkthrough

### Dashboard View
1. Navigate to the home page
2. Observe the elegant glassmorphic task cards with soft shadows
3. Notice the smooth hover effects and transitions
4. See how tasks are organized with priority and tag indicators

### Task Management
1. Click the floating action button (top right) to add a task
2. Fill in the task details in the modal
3. Notice the animated transitions and visual feedback
4. See the new task appear with a smooth animation

### Search, Filter & Sort
1. Use the search bar to filter tasks by keyword
2. Apply filters for priority, status, or tags
3. Change the sorting method using the sort dropdown
4. Observe how the task list updates with smooth animations

### Language Toggle
1. Click the language toggle button (top right)
2. Watch as all text throughout the application updates instantly
3. Notice that the language preference persists across sessions

## API Integration

### Backend Connection
The frontend connects to the FastAPI backend at the configured API base URL. All API calls use the following endpoints:

- `GET /api/tasks` - Retrieve all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task details
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

### Error Handling
- Network errors display user-friendly toast notifications
- Validation errors show inline feedback in forms
- Server errors provide appropriate messaging without exposing system details

## Testing the Application

### Manual Testing
1. **Task Creation**: Add several tasks with different priorities and tags
2. **Task Operations**: Test editing, deleting, and marking tasks as complete
3. **Filtering**: Apply various filters and verify correct results
4. **Sorting**: Test different sorting options
5. **Language Toggle**: Switch languages and verify all text updates
6. **Responsive Design**: Test on different screen sizes

### Visual Quality Checks
1. Verify glassmorphic cards render correctly with backdrop blur
2. Confirm hover effects (scale-105 + shadow-md) work properly
3. Check that animations are smooth and not jarring
4. Ensure text has proper contrast for accessibility
5. Verify that loading skeletons appear during API calls

## Development Commands

### Running in Development
```bash
npm run dev
```

### Building for Production
```bash
npm run build
```

### Running Tests
```bash
npm run test
```

### Linting
```bash
npm run lint
```

### Formatting Code
```bash
npm run format
```

## Troubleshooting

### Common Issues

**Issue**: Glassmorphic effects don't appear correctly
**Solution**: Ensure the browser supports backdrop-filter CSS property

**Issue**: API calls fail
**Solution**: Verify the `NEXT_PUBLIC_API_BASE_URL` is correctly configured and the backend server is running

**Issue**: Language toggle doesn't work
**Solution**: Check that translation data is properly loaded in the LanguageContext

**Issue**: Animations are janky
**Solution**: Consider performance optimization for complex animations on lower-end devices

## Performance Tips

- Use skeleton loaders to maintain perceived performance
- Implement optimistic UI updates for responsive feel
- Optimize images and assets for faster loading
- Test on various device capabilities to ensure smooth experience

## Next Steps

1. Explore the component library in the codebase
2. Review the API client implementation for integration patterns
3. Examine the internationalization setup for multi-language support
4. Look at the responsive design implementation for mobile compatibility