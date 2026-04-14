from fastapi import APIRouter
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.schemas.finance import BudgetCreate, BudgetUpdate, BudgetRead, BudgetStatus
from app.services import budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/", response_model=list[BudgetRead])
def list_budgets(current_user: AuthDep, db: SessionDep):
    return budget_service.get_budgets(db, current_user.id)


@router.get("/status", response_model=list[BudgetStatus])
def budget_status(current_user: AuthDep, db: SessionDep):
    return budget_service.get_budget_status(db, current_user.id)


@router.post("/", response_model=BudgetRead, status_code=201)
def add_budget(data: BudgetCreate, current_user: AuthDep, db: SessionDep):
    return budget_service.create_budget(db, current_user.id, data)


@router.put("/{budget_id}", response_model=BudgetRead)
def edit_budget(budget_id: int, data: BudgetUpdate, current_user: AuthDep, db: SessionDep):
    return budget_service.update_budget(db, budget_id, current_user.id, data)


@router.delete("/{budget_id}")
def remove_budget(budget_id: int, current_user: AuthDep, db: SessionDep):
    budget_service.delete_budget(db, budget_id, current_user.id)
    return {"message": "Deleted"}