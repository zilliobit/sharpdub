from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from .security import SECRET_KEY, ALGORITHM
from core.config import settings

COOKIE_NAME = "__Secure-access_token"
AUDIENCE = f"{settings.APP_NAME.lower()}-access"


def get_current_user(request: Request):
    """
    Reads the __Secure-access_token HttpOnly cookie set on login/signup.
    Returns the decoded JWT payload dict.
    """
    auth_token = request.cookies.get(COOKIE_NAME)

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(
            auth_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload  # callers can use payload["sub"], payload["sid"], etc.
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc


def require_roles(*roles: str):
    """
    Usage:  Depends(require_roles("admin", "moderator"))
    NOTE:   Roles must be stored in the JWT under the "roles" claim.
    """
    def checker(payload: dict = Depends(get_current_user)):
        user_roles: list = payload.get("roles", [])
        if not set(user_roles).intersection(roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return payload

    return checker


def get_current_user_id(payload: dict = Depends(get_current_user)) -> str:
    """Convenience dep — returns just the user UUID string."""
    return payload["sub"]
