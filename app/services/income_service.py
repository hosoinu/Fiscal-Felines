from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories import income_repo
from app.models.all_models import Income
from app.schemas.finance import IncomeCreate, IncomeUpdate


def get_income(session: Session, user_id: int) -> list[Income]:
    return income_repo.get_all(session, user_id)


def create_income(session: Session, user_id: int, data: IncomeCreate) -> Income:
    return income_repo.create(
        session=session,
        user_id=user_id,
        source=data.source,
        amount=data.amount,
        income_date=data.income_date or date.today(),
        is_recurring=data.is_recurring,
    )


def update_income(session: Session, income_id: int, user_id: int, data: IncomeUpdate) -> Income:
    i = income_repo.get_by_id(session, income_id)
    if not i or i.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income entry not found")
    return income_repo.update(session, i, **data.model_dump(exclude_unset=True))


def delete_income(session: Session, income_id: int, user_id: int) -> None:
    i = income_repo.get_by_id(session, income_id)
    if not i or i.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income entry not found")
    income_repo.delete(session, i)