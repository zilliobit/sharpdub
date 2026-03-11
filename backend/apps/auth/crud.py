from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Role
import uuid


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    res = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    return res.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    f_name: str,
    l_name: str,
    email: str,
    password_hash: str | None,
) -> User:
    user = User(
        f_name=f_name,
        l_name=l_name,
        email=email,
        password_hash=password_hash,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def assign_role(db: AsyncSession, user: User, role_name: str):
    role = (await db.execute(select(Role).where(Role.name == role_name))).scalar_one()
    user.roles.append(role)
    await db.commit()
