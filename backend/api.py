from fastapi import APIRouter
from apps.auth.routes import router as auth_router
from apps.todos.routes import router as todos_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(todos_router)