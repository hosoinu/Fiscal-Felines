from sqlmodel import Session, select
from typing import Optional
from app.models.all_models import Budget, CategoryEnum


def get_all(session: Session, user_id: int) -> list[Budget]:
    return list(session.exec(select(Budget).where(Budget.user_id == user_id)).all())


def get_by_id(session: Session, budget_id: int) -> Optional[Budget]:
    return session.get(Budget, budget_id)


def get_for_month(session: Session, user_id: int, month: int, year: int) -> list[Budget]:
    return list(session.exec(
        select(Budget).where(
            Budget.user_id == user_id,
            Budget.month == month,
            Budget.year == year,
        )
    ).all())


def create(session: Session, user_id: int, category: CategoryEnum,
           limit_amount: float, month: int, year: int) -> Budget:
    b = Budget(category=category, limit_amount=limit_amount,
               month=month, year=year, user_id=user_id)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


def update(session: Session, budget: Budget, **kwargs) -> Budget:
    for k, v in kwargs.items():
        if v is not None:
            setattr(budget, k, v)
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


def delete(session: Session, budget: Budget) -> None:
    session.delete(budget)
    session.commit()