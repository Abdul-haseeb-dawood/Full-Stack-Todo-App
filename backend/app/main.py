import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.routers.auth import router as auth_router
import uvicorn
from app.db.database import engine
from app.db.base import Base

# Import all models to ensure they are registered with SQLAlchemy
from app.models import Task, User  # noqa: F401


app = FastAPI(
    title="Todo API",
    description="A simple todo application backend with full CRUD functionality",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the tasks router
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

# Include the auth router
app.include_router(auth_router)


# Create all tables if they don't exist
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)