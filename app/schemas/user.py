from sqlmodel import SQLModel
from typing import Optional


class UserCreate(SQLModel):
    username: str
    password: str


class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(SQLModel):
    id: int
    username: str


class SignupRequest(SQLModel):
    username: str
    password: str