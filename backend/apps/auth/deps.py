from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from .security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

# This tells Swagger where to send the user to login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    auth_token = request.cookies.get("token") or token
    if not auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth token")
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id  # string of UUID
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_roles(*roles):
    def checker(user=Depends(get_current_user)):
        if not set(user["roles"]).intersection(roles):
            raise HTTPException(403)
        return user
    return checker
