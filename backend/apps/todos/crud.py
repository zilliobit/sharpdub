from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Todo
from .schemas import TodoCreate, TodoUpdate

async def create_todo(db: AsyncSession, todo: TodoCreate):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return result.scalars().all()

async def get_todo_by_id(db: AsyncSession, todo_id: int):
    return await db.get(Todo, todo_id)

async def update_todo(db: AsyncSession, todo_id: int, todo_in: TodoUpdate):
    db_todo = await db.get(Todo, todo_id)
    if db_todo:
        update_data = todo_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        await db.commit()
        await db.refresh(db_todo)
    return db_todo

async def delete_todo(db: AsyncSession, todo_id: int):
    db_todo = await db.get(Todo, todo_id)
    if db_todo:
        await db.delete(db_todo)
        await db.commit()
        return True
    return False