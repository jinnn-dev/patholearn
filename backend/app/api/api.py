from fastapi import APIRouter

from app.api.endpoints import login, users, courses, task_groups, base_task, task, annotations

"""
Definition of all available API-Routes
"""

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(task_groups.router, prefix='/taskgroups', tags=["taskgroups"])
api_router.include_router(base_task.router, prefix='/tasks', tags=["tasks"])
api_router.include_router(task.router, prefix='/tasks/task', tags=["task"])
api_router.include_router(annotations.router, prefix='/annotations', tags=["annotations"])
