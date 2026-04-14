from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories import budget_repo, expense_repo
from app.models.all_models import Budget
from app.schemas.finance import BudgetCreate, BudgetUpdate, BudgetStatus


def get_budgets(session: Session, user_id: int) -> list[Budget]:
    return budget_repo.get_all(session, user_id)


def create_budget(session: Session, user_id: int, data: BudgetCreate) -> Budget:
    return budget_repo.create(
        session=session,
        user_id=user_id,
        category=data.category,
        limit_amount=data.limit_amount,
        month=data.month,
        year=data.year,
    )


def update_budget(session: Session, budget_id: int, user_id: int, data: BudgetUpdate) -> Budget:
    b = budget_repo.get_by_id(session, budget_id)
    if not b or b.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget_repo.update(session, b, **data.model_dump(exclude_unset=True))


def delete_budget(session: Session, budget_id: int, user_id: int) -> None:
    b = budget_repo.get_by_id(session, budget_id)
    if not b or b.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    budget_repo.delete(session, b)


def get_budget_status(session: Session, user_id: int) -> list[BudgetStatus]:
    now = date.today()
    budgets = budget_repo.get_for_month(session, user_id, now.month, now.year)
    result = []
    for b in budgets:
        spent = expense_repo.total_by_category_month(
            session, user_id, b.category, now.month, now.year
        )
        result.append(BudgetStatus(
            id=b.id,
            category=b.category,
            limit_amount=b.limit_amount,
            spent=round(spent, 2),
            remaining=round(b.limit_amount - spent, 2),
            over_budget=spent > b.limit_amount,
        ))
    return result