from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from .deps import get_current_user
from . import crud

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def get_me(
    payload: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the currently authenticated user's profile.
    Protected — requires valid __Secure-access_token cookie.
    """
    user = await crud.get_user_by_id(db, payload["sub"])
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": str(user.id),
            "f_name": user.f_name,
            "l_name": user.l_name,
            "email": user.email,
            "roles": [role.name for role in user.roles] if user.roles else [],
        }
    }
