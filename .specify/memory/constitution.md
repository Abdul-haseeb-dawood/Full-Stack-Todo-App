<!--
Sync Impact Report:
- Version change: N/A → v1.0.0
- Added sections: Project Overview, Core Features & REST API Endpoints, Non-Functional Requirements, Technology Stack, Monorepo Structure, Development Workflow, Guiding Principles, Deliverables & Success Criteria
- Templates requiring updates: ✅ All templates updated as this is the initial constitution
- Follow-up TODOs: None
-->

# The Evolution of Todo - Phase II Constitution

## Project Overview

The Evolution of Todo - Phase II represents a significant advancement from the original Phase I in-memory console application to a sophisticated, full-stack web application. This evolution transforms a simple command-line tool into a visually stunning, professional-grade task management system that demonstrates modern web development capabilities. The application is designed to impress hackathon judges with its luxurious UI, while providing comprehensive task management functionality including CRUD operations, priorities, tags, search, filtering, sorting, and recurring tasks. The project emphasizes both technical excellence and visual polish, preparing for future Phase III chatbot integration.

The MVP focus centers on delivering a complete task management experience with CRUD operations, priority and tag systems (high/medium/low, work/home), advanced search and filtering capabilities, flexible sorting options, recurring task functionality, and a global language toggle. The UI excellence goal prioritizes professional polish, intuitive layout, and luxurious design elements including glassmorphic cards, smooth hover effects, soft shadows, and responsive grid layouts that create a premium user experience.

## Core Features & REST API Endpoints

### Core Features
- **CRUD Tasks**: Complete Create, Read, Update, Delete functionality with optimistic UI updates
- **Priorities & Tags**: Support for high/medium/low priority levels and work/home categories
- **Search & Filter**: Advanced filtering by keyword, status, priority, or date
- **Sorting**: Multiple sorting options including due date, priority, and alphabetical
- **Recurring Tasks**: Auto-rescheduling of repeating tasks with configurable recurrence patterns
- **Language Toggle**: Dynamic site-wide language change without page refresh

### REST API Endpoints

| Method | Path | Description | Request Body | Response | Notes |
|--------|------|-------------|--------------|---------|-------|
| GET    | /api/tasks | List all tasks | optional query: status, priority, due_date, keyword | array of Task objects | Filter/sort supported |
| POST   | /api/tasks | Create new task | title, description, priority, tags, due_date, recurrence | created Task object | Optimistic UI |
| GET    | /api/tasks/{id} | Get task details | none | Task object | |
| PUT    | /api/tasks/{id} | Update task fully | title, description, priority, tags, due_date, recurrence | updated Task object | |
| DELETE | /api/tasks/{id} | Delete task | none | confirmation | |
| PATCH  | /api/tasks/{id}/complete | Toggle completed | none | updated Task object | Animated checkmark in UI |

### Task Object Model
```
{
  "id": string,
  "title": string,
  "description": string,
  "priority": "high" | "medium" | "low",
  "tags": string[],
  "completed": boolean,
  "due_date": string | null,
  "recurrence": {
    "type": "daily" | "weekly" | "monthly" | "yearly" | null,
    "interval": number
  } | null,
  "created_at": string,
  "updated_at": string
}
```

## Non-Functional Requirements

- **Clean, Modular Code**: TypeScript for frontend and Python for backend with clear separation of concerns
- **Type Safety**: Strong typing with interfaces for Task, Priority, Tag, and API response objects
- **Responsive UI**: Mobile-first design supporting 320px+ screens, tablets, and desktops
- **Error Handling**: User-friendly error messages with appropriate HTTP status codes
- **Performance**: Skeleton loaders, minimal re-renders, and optimized data fetching
- **Accessibility**: ARIA labels, focus indicators, and keyboard navigation support
- **Maintainable Architecture**: Scalable structure that supports future feature additions

## Technology Stack

- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS, and React Server/Client components as needed
- **Backend**: Python 3.11+, FastAPI for API framework, SQLModel for database modeling, asyncpg for PostgreSQL connectivity
- **Database**: Neon Serverless PostgreSQL for persistent data storage with automatic scaling
- **Spec-Driven Development**: Qwen-cli and Spec-Kit Plus for specification-driven development workflow
- **Dev Tools**: Docker Compose for local development environment, layered QWEN.md files for documentation

## Monorepo Structure

The project follows a strict monorepo structure with clear separation between frontend and backend:

```
root/
├── frontend/                 # Next.js application
├── backend/                  # FastAPI application
├── specs/                    # Specification files
│   ├── api/                  # API specifications
│   ├── ui/                   # UI/UX specifications
│   ├── database/             # Database schema specifications
│   └── features/             # Feature specifications
├── .spec-kit/config.yaml     # Spec-kit configuration
├── docker-compose.yml        # Combined development environment
├── frontend/QWEN.md          # Frontend-specific guidance
├── backend/QWEN.md           # Backend-specific guidance
└── QWEN.md                   # Root project vision
```

## Development Workflow

The project follows a strict spec-first agentic workflow that ensures comprehensive planning before implementation:

1. **Constitution** → Establish project governance and principles
2. **Specifications** → Detailed feature and technical specifications
3. **Planning** → Implementation plan with tasks and milestones
4. **Task Execution** → Agent-driven development of individual features
5. **Implementation** → Code generation and integration

No manual coding is permitted; all code must be generated via Qwen agents to ensure consistency and adherence to specifications. Mandatory checkpoints are required at major feature implementations: Dashboard layout, CRUD operations, recurring tasks, and language toggle functionality.

## Guiding Principles

### I. Spec-First Development
All features must be fully specified before implementation begins. Specifications must include detailed requirements, API contracts, UI mockups, and acceptance criteria. This ensures comprehensive planning and reduces rework during implementation.

### II. Stunning UI as Top Priority
Visual excellence is paramount and must be prioritized throughout development. The UI must incorporate glassmorphic cards, hover lifts, soft shadows, smooth transitions, and consistent spacing rhythm to create a luxurious user experience that impresses judges and users alike.

### III. Accessibility and Responsiveness by Design
All UI components must be accessible from the start, incorporating ARIA labels, focus indicators, and keyboard navigation. The design must be responsive across all device sizes from mobile (320px+) to desktop, ensuring a consistent experience.

### IV. Future-Proof Architecture
The codebase must be structured to support future Phase III chatbot integration. This includes modular design, clear API boundaries, and extensible data models that can accommodate additional functionality without major refactoring.

### V. Transparency for Hackathon Judging
All development decisions, architectural choices, and implementation details must be clearly documented. The codebase should be self-explanatory and showcase the team's technical capabilities and thoughtful design decisions.

## Deliverables & Success Criteria

- **Fully Integrated Frontend/Backend**: Working Next.js frontend and FastAPI backend with seamless integration
- **Complete Task Functionality**: All CRUD operations with priorities, tags, search/filter, sorting, and recurring tasks working correctly
- **Global Language Toggle**: Site-wide language change functionality working without page refresh
- **Luxurious UI**: Beautiful, responsive, demo-ready interface that creates immediate visual impact
- **Persistent Data**: Reliable data storage and retrieval using Neon PostgreSQL
- **Clean, Type-Safe Code**: Well-structured, maintainable code generated by agents with proper type safety
- **Comprehensive Specifications**: Complete history of specifications in the /specs directory
- **Docker Setup**: Simple docker-compose setup for easy full-stack application deployment
- **Agent Reference Document**: Markdown constitution.md version v1.0 at root for agent guidance

## Governance

This constitution serves as the authoritative governance document for The Evolution of Todo - Phase II project. All development practices, architectural decisions, and implementation choices must align with the principles and requirements outlined in this document. Any deviations must be documented with clear justification and approved by the project leadership.

Amendments to this constitution require formal documentation of the changes, approval from project stakeholders, and a migration plan for existing code and specifications. All pull requests and code reviews must verify compliance with constitutional requirements. The constitution supersedes all other development practices and guidelines.

**Version**: v1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
