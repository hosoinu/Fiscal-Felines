from sqlmodel import Session, select, func
from typing import Optional
from datetime import date
from app.models.all_models import Expense, CategoryEnum


def get_all(session: Session, user_id: int, category: Optional[CategoryEnum] = None) -> list[Expense]:
    q = select(Expense).where(Expense.user_id == user_id)
    if category:
        q = q.where(Expense.category == category)
    return list(session.exec(q.order_by(Expense.expense_date.desc())).all())


def get_by_id(session: Session, expense_id: int) -> Optional[Expense]:
    return session.get(Expense, expense_id)


def create(session: Session, user_id: int, title: str, amount: float,
           category: CategoryEnum, expense_date: date, notes: Optional[str]) -> Expense:
    e = Expense(title=title, amount=amount, category=category,
                expense_date=expense_date, notes=notes, user_id=user_id)
    session.add(e)
    session.commit()
    session.refresh(e)
    return e


def update(session: Session, expense: Expense, **kwargs) -> Expense:
    for k, v in kwargs.items():
        if v is not None:
            setattr(expense, k, v)
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


def delete(session: Session, expense: Expense) -> None:
    session.delete(expense)
    session.commit()


def total_all(session: Session, user_id: int) -> float:
    r = session.exec(
        select(func.sum(Expense.amount)).where(Expense.user_id == user_id)
    ).first()
    return float(r or 0)


def total_by_category_month(session: Session, user_id: int,
                             category: CategoryEnum, month: int, year: int) -> float:
    r = session.exec(
        select(func.sum(Expense.amount)).where(
            Expense.user_id == user_id,
            Expense.category == category,
            func.strftime("%m", Expense.expense_date) == f"{month:02d}",
            func.strftime("%Y", Expense.expense_date) == str(year),
        )
    ).first()
    return float(r or 0)


def category_totals(session: Session, user_id: int) -> list[dict]:
    rows = session.exec(
        select(Expense.category, func.sum(Expense.amount).label("total"))
        .where(Expense.user_id == user_id)
        .group_by(Expense.category)
    ).all()
    return [{"category": r[0], "total": round(float(r[1]), 2)} for r in rows]


def monthly_totals(session: Session, user_id: int) -> list[dict]:
    rows = session.exec(
        select(
            func.strftime("%Y-%m", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("total"),
        )
        .where(Expense.user_id == user_id)
        .group_by(func.strftime("%Y-%m", Expense.expense_date))
        .order_by(func.strftime("%Y-%m", Expense.expense_date).desc())
    ).all()
    return [{"month": r[0], "total": round(float(r[1]), 2)} for r in rows[:6]][::-1]