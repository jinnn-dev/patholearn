from app.api.endpoints import info_images, slides, task_images
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(slides.router, prefix="/slides", tags=["slides"])
api_router.include_router(task_images.router, prefix="/task-images", tags=["taskImages"])
api_router.include_router(info_images.router, prefix="/infoImages", tags=["infoImages"])
