from fastapi import APIRouter
from app.router.endpoints import projects, datasets, tasks, builder

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(builder.router, prefix="/builder", tags=["builder"])
