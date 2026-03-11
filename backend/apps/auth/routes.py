from fastapi import APIRouter, Depends, Response, Request
from . import schemas, services
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from core.rate_limit import rate_limit
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", dependencies=[Depends(rate_limit)])
async def login(
    data: schemas.LoginSchema,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """
    Password-based login. Returns secure HttpOnly cookies on success.
    """
    access_token, refresh_token, csrf_token = await services.login_with_password(db, data)

    response.set_cookie(
        key="__Secure-access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
    response.set_cookie(
        key="__Secure-refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
    response.set_cookie(
        key="__Host-csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="strict",
        path="/",
    )

    return {"success": True}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("__Secure-access_token", path="/")
    response.delete_cookie("__Secure-refresh_token", path="/")
    response.delete_cookie("__Host-csrf_token", path="/")
    return {"success": True}


@router.post("/signup", dependencies=[Depends(rate_limit)])
async def signup(
    request: Request,
    payload: schemas.SignupSchema,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    result = await services.signup_request(request, payload, response, background_tasks, db)
    return JSONResponse(status_code=result.get("status", 200), content=result)


@router.post("/signup/verify")
async def signup_verify(
    request: Request,
    payload: schemas.SignupVerifySchema,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    access_token, refresh_token, csrf_token = await services.signup_verify(
        request, payload, response, db
    )

    response.set_cookie(
        key="__Secure-access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
    response.set_cookie(
        key="__Secure-refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
    response.set_cookie(
        key="__Host-csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="strict",
        path="/",
    )

    return {"success": True}


@router.post("/resend-otp", dependencies=[Depends(rate_limit)])
async def resend_otp(
    data: schemas.EmailSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    await services.resend_signup_otp(db, data.email, background_tasks)
    return {"success": True}
