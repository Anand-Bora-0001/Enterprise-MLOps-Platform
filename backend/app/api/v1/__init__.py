from fastapi import APIRouter
from app.api.v1 import auth, users, projects, datasets, experiments, registry, explain

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(registry.router, prefix="/registry", tags=["registry"])
api_router.include_router(explain.router, prefix="/explain", tags=["explain"])
