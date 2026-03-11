from fastapi import APIRouter, Depends, Response, Request
from . import schemas, services
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from .security import create_access_token
from core.rate_limit import rate_limit
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", dependencies=[Depends(rate_limit)])
async def login(data: schemas.EmailSchema, background_tasks: BackgroundTasks, db=Depends(get_db)):
    await services.request_otp(db, data.email, background_tasks)
    return {"sent": True}

@router.post("/verify")
async def verify( data: schemas.OTPVerify, response: Response, db: AsyncSession = Depends(get_db)):
    user = await services.verify_otp(db, data.email, data.otp)

    token = create_access_token(user)

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {"ok": True}

@router.post("/signup", dependencies=[Depends(rate_limit)])
async def signup(
    request: Request,
    payload: schemas.SignupSchema,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    result = await services.signup_request(request, payload, response, background_tasks, db)

    return JSONResponse(
        status_code=result.get("status", 200),
        content=result
    )

@router.post("/signup/verify")
async def signup_verify(
    request: Request,
    payload: schemas.SignupVerifySchema,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    
    access_token, refresh_token, csrf_token = await services.signup_verify(request, payload, response, db)

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

