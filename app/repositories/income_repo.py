from sqlmodel import Session, select, func
from typing import Optional
from datetime import date
from app.models.all_models import Income


def get_all(session: Session, user_id: int) -> list[Income]:
    return list(session.exec(
        select(Income).where(Income.user_id == user_id).order_by(Income.income_date.desc())
    ).all())


def get_by_id(session: Session, income_id: int) -> Optional[Income]:
    return session.get(Income, income_id)


def create(session: Session, user_id: int, source: str, amount: float,
           income_date: date, is_recurring: bool) -> Income:
    i = Income(source=source, amount=amount, income_date=income_date,
               is_recurring=is_recurring, user_id=user_id)
    session.add(i)
    session.commit()
    session.refresh(i)
    return i


def update(session: Session, income: Income, **kwargs) -> Income:
    for k, v in kwargs.items():
        if v is not None:
            setattr(income, k, v)
    session.add(income)
    session.commit()
    session.refresh(income)
    return income


def delete(session: Session, income: Income) -> None:
    session.delete(income)
    session.commit()


def total_all(session: Session, user_id: int) -> float:
    r = session.exec(
        select(func.sum(Income.amount)).where(Income.user_id == user_id)
    ).first()
    return float(r or 0)