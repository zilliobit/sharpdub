from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from . import crud
from .schemas import TodoCreate, TodoUpdate

async def get_all_todos(db: AsyncSession, skip: int, limit: int):
    return await crud.get_todos(db, skip, limit)

async def create_new_todo(db: AsyncSession, todo_in: TodoCreate):
    return await crud.create_todo(db, todo_in)

async def get_single_todo(db: AsyncSession, todo_id: int):
    todo = await crud.get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

async def update_todo_item(db: AsyncSession, todo_id: int, todo_in: TodoUpdate):
    todo = await crud.update_todo(db, todo_id, todo_in)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

async def remove_todo(db: AsyncSession, todo_id: int):
    success = await crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}