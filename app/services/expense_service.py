from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories import expense_repo
from app.models.all_models import Expense, CategoryEnum
from app.schemas.finance import ExpenseCreate, ExpenseUpdate


def get_expenses(session: Session, user_id: int, category: CategoryEnum = None) -> list[Expense]:
    return expense_repo.get_all(session, user_id, category)


def create_expense(session: Session, user_id: int, data: ExpenseCreate) -> Expense:
    return expense_repo.create(
        session=session,
        user_id=user_id,
        title=data.title,
        amount=data.amount,
        category=data.category,
        expense_date=data.expense_date or date.today(),
        notes=data.notes,
    )


def update_expense(session: Session, expense_id: int, user_id: int, data: ExpenseUpdate) -> Expense:
    e = expense_repo.get_by_id(session, expense_id)
    if not e or e.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense_repo.update(session, e, **data.model_dump(exclude_unset=True))


def delete_expense(session: Session, expense_id: int, user_id: int) -> None:
    e = expense_repo.get_by_id(session, expense_id)
    if not e or e.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    expense_repo.delete(session, e)