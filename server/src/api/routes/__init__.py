"""API routes."""

from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .projects import router as projects_router
from .contributions import router as contributions_router
from .badges import router as badges_router

# Create main router
api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(projects_router)
api_router.include_router(contributions_router)
api_router.include_router(badges_router)

__all__ = ["api_router"]