from fastapi import APIRouter

from app.api.endpoints import slides

"""
Definition of all available API-Routes
"""

api_router = APIRouter()
api_router.include_router(slides.router, prefix="/slides", tags=["slides"])
