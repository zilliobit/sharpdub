from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession # Use AsyncSession
from db.deps import get_db
from .schemas import TodoCreate, TodoUpdate, TodoOut
from . import services # Assuming your CRUD functions are here
from apps.auth.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoOut)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_new_todo(db, todo)

@router.get("/", response_model=list[TodoOut])
async def read_todos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await services.get_all_todos(db, skip, limit)

@router.get("/{todo_id}", response_model=TodoOut)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_single_todo(db, todo_id)

@router.put("/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    return await services.update_todo_item(db, todo_id, todo)

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    return await services.remove_todo(db, todo_id)