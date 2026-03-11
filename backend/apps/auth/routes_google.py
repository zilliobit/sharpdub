from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from core.oauth import oauth
from .services_google import google_login

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])

@router.get("/login")
async def google_login_redirect(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri=request.url_for("google_callback")
    )

@router.get("/callback", name="google_callback")
async def google_callback(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    token_id = await google_login(db, user_info)

    # 3. Create the Redirect Response to your Nuxt app
    # In development, this is likely http://localhost:3000
    #frontend_url = "http://localhost:3000/dashboard" 
    #redirect_response = RedirectResponse(url=frontend_url)

    response.set_cookie(
        key="token",
        value=token_id,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {"success": True}
