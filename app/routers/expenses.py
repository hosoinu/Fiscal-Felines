from fastapi import APIRouter
from typing import Optional
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.models.finance import CategoryEnum
from app.schemas.finance import ExpenseCreate, ExpenseUpdate, ExpenseRead
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/", response_model=list[ExpenseRead])
def list_expenses(current_user: AuthDep, db: SessionDep, category: Optional[CategoryEnum] = None):
    return expense_service.get_expenses(db, current_user.id, category)


@router.post("/", response_model=ExpenseRead, status_code=201)
def add_expense(data: ExpenseCreate, current_user: AuthDep, db: SessionDep):
    return expense_service.create_expense(db, current_user.id, data)


@router.put("/{expense_id}", response_model=ExpenseRead)
def edit_expense(expense_id: int, data: ExpenseUpdate, current_user: AuthDep, db: SessionDep):
    return expense_service.update_expense(db, expense_id, current_user.id, data)


@router.delete("/{expense_id}")
def remove_expense(expense_id: int, current_user: AuthDep, db: SessionDep):
    expense_service.delete_expense(db, expense_id, current_user.id)
    return {"message": "Deleted"}