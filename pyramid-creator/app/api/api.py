from fastapi import APIRouter

from app.api.endpoints import slides, task_images

api_router = APIRouter()
api_router.include_router(slides.router, prefix="/slides", tags=["slides"])
api_router.include_router(task_images.router, prefix="/task-images", tags=["task-images"])
