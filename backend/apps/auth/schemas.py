from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class TOTPVerify(BaseModel):
    code: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    roles: list[str]

    class Config:
        from_attributes = True

class SignupSchema(BaseModel):
    f_name: str
    l_name: str
    email: EmailStr
    password: str

    class Config:
        extra = "ignore"

class SignupVerifySchema(BaseModel):
    email: EmailStr
    otp: str