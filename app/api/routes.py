from fastapi import APIRouter
from app.api.endpoints import auth, users, jobs, candidates, resumes

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
