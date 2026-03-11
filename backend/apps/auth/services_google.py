from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .security import create_access_token

async def google_login(db: AsyncSession, user_info: dict) -> str:
    email = user_info.get("email")
    name = user_info.get("name")
    email_verified = user_info.get("email_verified")

    if not email or not email_verified:
        raise HTTPException(400, "Google account not verified")

    user = await crud.get_user_by_email(db, email)
    if not user:
        user = await crud.create_user(db, name=name, email=email, password_hash=None)


    token = create_access_token({
        "sub": str(user.id),   # UUID MUST be string
        "email": user.email,
    })

    return token
