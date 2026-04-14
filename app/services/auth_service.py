from sqlmodel import Session
from fastapi import HTTPException, status
from app.repositories.user import UserRepository


class AuthService:

    @staticmethod
    def signup(session: Session, username: str, password: str, hash_fn, create_token_fn) -> str:
        repo = UserRepository(session)

        existing = repo.get_by_username(username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        hashed = hash_fn(password)
        repo.create_user(username, hashed)

        flash_msg = "Registration completed! Sign in now!"
        return flash_msg

    @staticmethod
    def login(session: Session, username: str, password: str, verify_fn, create_token_fn) -> str:
        repo = UserRepository(session)

        user = repo.get_by_username(username)
        if not user or not verify_fn(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return create_token_fn({"sub": user.username})