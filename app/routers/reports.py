from fastapi import APIRouter
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.services import reports_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def summary(current_user: AuthDep, db: SessionDep):
    return reports_service.get_summary(db, current_user.id)


@router.get("/by-category")
def by_category(current_user: AuthDep, db: SessionDep):
    return reports_service.get_by_category(db, current_user.id)


@router.get("/monthly-trend")
def monthly_trend(current_user: AuthDep, db: SessionDep):
    return reports_service.get_monthly_trend(db, current_user.id)