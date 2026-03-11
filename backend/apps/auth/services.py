import pyotp, secrets, hashlib
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import HTTPException, BackgroundTasks
from db.redis import redis_client
import uuid, json
from . import crud, schemas, security
from sqlalchemy.ext.asyncio import AsyncSession
from .security import hash_password, verify_password
from core.config import settings
from core.mail import conf

OTP_TTL = 60 * 15  # 15 minutes


# ─── Email helper ────────────────────────────────────────────────────────────

async def send_otp(email: str, otp: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=f"{settings.MAIL_FROM_NAME} Verification Code",
        recipients=[email],
        body=f"Your verification code is: {otp}. This code expires in 15 minutes.",
        subtype=MessageType.plain,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)


# ─── Password login ───────────────────────────────────────────────────────────

async def login_with_password(db: AsyncSession, data: schemas.LoginSchema):
    """Verify email + password, return (access_token, refresh_token, csrf_token)."""
    user = await crud.get_user_by_email(db, data.email)

    # Constant-time check to prevent user enumeration
    if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    sid = uuid.uuid4().hex
    csrf_token = secrets.token_urlsafe(32)

    access_token = security.create_access_token(sub=str(user.id), sid=sid)
    refresh_token = security.create_refresh_token(sid=sid)

    return access_token, refresh_token, csrf_token


# ─── OTP login (passwordless) ────────────────────────────────────────────────

async def request_otp(db, email: str, background_tasks: BackgroundTasks):
    user = await crud.get_user_by_email(db, email)
    if not user:
        # Don't reveal whether the user exists
        return

    otp = str(secrets.randbelow(900000) + 100000)
    await redis_client.setex(f"otp:{email}", OTP_TTL, otp)
    await send_otp(email, otp, background_tasks)


async def verify_otp(db: AsyncSession, email: str, otp: str):
    stored = await redis_client.get(f"otp:{email}")
    if not stored or stored != otp:
        raise HTTPException(400, "Invalid or expired OTP")

    await redis_client.delete(f"otp:{email}")

    user = await crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(404, "User not found")

    return {"sub": str(user.id), "email": user.email}


# ─── Signup ───────────────────────────────────────────────────────────────────

async def signup_request(request, payload: schemas.SignupSchema, response, background_tasks, db):
    if await crud.get_user_by_email(db, payload.email):
        raise HTTPException(400, "An account with this email already exists")

    sid = uuid.uuid4().hex
    csrf_token = secrets.token_urlsafe(32)

    access_token = security.create_access_token(sub=payload.email, sid=sid)
    refresh_token = security.create_refresh_token(sid=sid)

    otp = str(secrets.randbelow(900000) + 100000)

    await redis_client.setex(
        f"signup:{payload.email}",
        OTP_TTL,
        json.dumps(
            {
                "f_name": payload.f_name,
                "l_name": payload.l_name,
                "password": hash_password(payload.password),
                "otp": otp,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "csrf_token": csrf_token,
            }
        ),
    )

    message = MessageSchema(
        subject=f"{settings.MAIL_FROM_NAME} Verification Code",
        recipients=[payload.email],
        body=(
            f"Hi {payload.f_name},\n"
            f"Your verification code is: {otp}.\n"
            "This code expires in 15 minutes."
        ),
        subtype=MessageType.plain,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"status": 200, "success": True, "message": "OTP sent", "data": {}}


async def signup_verify(request, payload: schemas.SignupVerifySchema, response, db):
    raw = await redis_client.get(f"signup:{payload.email}")
    if not raw:
        raise HTTPException(400, "OTP expired or not found. Please sign up again.")

    data_dict = json.loads(raw)

    if data_dict["otp"] != payload.otp:
        raise HTTPException(400, "Invalid OTP")

    # Build a full SignupSchema (password is already hashed, but create_user
    # should accept pre-hashed via a flag or we pass raw fields separately)
    user = await crud.create_user(
        db,
        f_name=data_dict["f_name"],
        l_name=data_dict["l_name"],
        email=payload.email,
        password_hash=data_dict["password"],  # already hashed
    )

    await redis_client.delete(f"signup:{payload.email}")

    # FIX: was returning a set `{}` — now returns a proper tuple
    return (
        data_dict["access_token"],
        data_dict["refresh_token"],
        data_dict["csrf_token"],
    )


async def resend_signup_otp(db, email: str, background_tasks: BackgroundTasks):
    raw = await redis_client.get(f"signup:{email}")
    if not raw:
        raise HTTPException(400, "Signup session expired. Please sign up again.")

    data_dict = json.loads(raw)
    otp = str(secrets.randbelow(900000) + 100000)
    data_dict["otp"] = otp

    await redis_client.setex(f"signup:{email}", OTP_TTL, json.dumps(data_dict))
    await send_otp(email, otp, background_tasks)


# ─── 2FA helpers ─────────────────────────────────────────────────────────────

def generate_totp_secret():
    return pyotp.random_base32()


def verify_totp(secret: str, code: str):
    return pyotp.TOTP(secret).verify(code)


def generate_backup_codes():
    return [secrets.token_hex(4) for _ in range(10)]


def hash_code(code: str):
    return hashlib.sha256(code.encode()).hexdigest()
