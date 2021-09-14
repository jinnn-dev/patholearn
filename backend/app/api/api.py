from fastapi import APIRouter

from app.api.endpoints import login, users, slides, courses, task_groups, tasks

"""
Definition of all available API-Routes
"""

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(slides.router, prefix="/slides", tags=["slides"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(task_groups.router, prefix='/taskgroups', tags=["taskgroups"])
api_router.include_router(tasks.router, prefix='/tasks', tags=["tasks"])
