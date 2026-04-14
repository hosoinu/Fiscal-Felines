from sqlmodel import Session, select, func
from app.models.user import User
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, password: str) -> User:
        try:
            user = User(username=username, password=password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            self.db.rollback()
            raise

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.exec(
            select(User).where(User.username == username)
        ).one_or_none()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_all_users(self) -> list[User]:
        return self.db.exec(select(User)).all()

    def search_users(self, query: str, page: int = 1, limit: int = 10) -> Tuple[list[User], Pagination]:
        offset = (page - 1) * limit
        stmt = select(User)

        if query:
            stmt = stmt.where(User.username.ilike(f"%{query}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.exec(count_stmt).one()

        users = self.db.exec(stmt.offset(offset).limit(limit)).all()

        pagination = Pagination(
            total_count=total,
            current_page=page,
            limit=limit
        )

        return users, pagination