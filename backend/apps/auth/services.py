import pyotp, secrets, hashlib
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, BackgroundTasks
from db.redis import redis_client
import uuid, json
from . import crud, dpop, services, schemas, security
from sqlalchemy.ext.asyncio import AsyncSession
from .security import hash_password
from core.config import settings
from core.mail import conf

OTP_TTL = 60*15

async def send_otp(email: str, otp: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=f"{settings.MAIL_FROM_NAME} Verification Code",
        recipients=[email],
        body=f"Your verification code is: {otp}. This code expires in 15 minutes.",
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

async def request_otp(db, email, background_tasks: BackgroundTasks):
    user = await crud.get_user_by_email(db, email) or await crud.create_user(db, email)

    otp = str(secrets.randbelow(900000) + 100000)
    await redis_client.setex(f"otp:{email}", OTP_TTL, otp)
    await send_otp(email, otp, background_tasks)

async def verify_otp(db: AsyncSession, email: str, otp: str):
    stored = await redis_client.get(f"otp:{email}")
    if stored != otp:
        raise HTTPException(400, "Invalid OTP")

    await redis_client.delete(f"otp:{email}")

    user = await crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(404, "User not found")

    return {
        "sub": str(user.id),   # UUID MUST be string
        "email": user.email,
    }

async def signup_request(request, payload, response, background_tasks, db):
    if await crud.get_user_by_email(db, payload.email):
        raise HTTPException(400, "User already exists")
    
    sid = uuid.uuid4().hex

    csrf_token = secrets.token_urlsafe(32)

    access_token = security.create_access_token(
        sub=payload.email,
        sid=sid
    )

    refresh_token = security.create_refresh_token(
        sid=sid
    )

    otp = str(secrets.randbelow(900000) + 100000)

    await redis_client.setex(
        f"signup:{payload.email}",
        OTP_TTL,
        json.dumps({
            "f_name": payload.f_name,
            "l_name": payload.l_name,
            "password": hash_password(payload.password),
            "otp": otp,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "csrf_token": csrf_token
        })
    )

    message = MessageSchema(
        subject=f"{settings.MAIL_FROM_NAME} Verification Code",
        recipients=[payload.email],
        body=(
            f"Hi {payload.f_name},\n"
            f"Your verification code is: {otp}.\n"
            "This code expires in 15 minutes."
        ),
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {
        "status": 200,
        "success": True,  # proper boolean, not string
        "message": "OTP sent",
        "data": {}
    }

async def signup_verify(request, payload, response, db):
    raw = await redis_client.get(f"signup:{payload.email}")
    if not raw:
        raise HTTPException(400, "OTP expired")

    data_dict = json.loads(raw)
    data_dict['email'] = payload.email

    if data_dict['otp'] != payload.otp:
        raise HTTPException(400, "Invalid OTP")

    data = schemas.SignupSchema(**data_dict)

    user = await crud.create_user(db, data)

    await redis_client.delete(f"signup:{payload.email}")
    
    return {
        data_dict['access_token'],
        data_dict['refresh_token'],
        data_dict['csrf_token'],
    }

# 2FA
def generate_totp_secret():
    return pyotp.random_base32()

def verify_totp(secret: str, code: str):
    return pyotp.TOTP(secret).verify(code)

def generate_backup_codes():
    return [secrets.token_hex(4) for _ in range(10)]

def hash_code(code: str):
    return hashlib.sha256(code.encode()).hexdigest()

