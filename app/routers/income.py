from fastapi import APIRouter
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.schemas.finance import IncomeCreate, IncomeUpdate, IncomeRead
from app.services import income_service

router = APIRouter(prefix="/income", tags=["Income"])


@router.get("/", response_model=list[IncomeRead])
def list_income(current_user: AuthDep, db: SessionDep):
    return income_service.get_income(db, current_user.id)


@router.post("/", response_model=IncomeRead, status_code=201)
def add_income(data: IncomeCreate, current_user: AuthDep, db: SessionDep):
    return income_service.create_income(db, current_user.id, data)


@router.put("/{income_id}", response_model=IncomeRead)
def edit_income(income_id: int, data: IncomeUpdate, current_user: AuthDep, db: SessionDep):
    return income_service.update_income(db, income_id, current_user.id, data)


@router.delete("/{income_id}")
def remove_income(income_id: int, current_user: AuthDep, db: SessionDep):
    income_service.delete_income(db, income_id, current_user.id)
    return {"message": "Deleted"}