from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import schemas
from .models import User, Role

async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def create_user(db: AsyncSession, data: schemas.SignupSchema) -> User:
    user = User(
        f_name=data.f_name,
        l_name=data.l_name,
        email=data.email,
        password_hash=data.password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def assign_role(db: AsyncSession, user: User, role_name: str):
    role = (await db.execute(select(Role).where(Role.name == role_name))).scalar_one()
    user.roles.append(role)
    await db.commit()
