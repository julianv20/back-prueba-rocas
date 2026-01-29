from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    id: str = Field(..., description="User ID (cedula)")
    name: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1, alias="lastName")
    email: EmailStr
    password: str = Field(..., min_length=6)
    
    class Config:
        populate_by_name = True


class UserResponse(BaseModel):
    id: str
    name: str
    lastName: str
    email: str
    token: Optional[str] = None
    
    class Config:
        populate_by_name = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
