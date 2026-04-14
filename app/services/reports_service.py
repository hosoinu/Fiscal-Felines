from sqlmodel import Session
from app.repositories import expense_repo, income_repo, subscription_repo


def get_summary(session: Session, user_id: int) -> dict:
    total_income = income_repo.total_all(session, user_id)
    total_expenses = expense_repo.total_all(session, user_id)
    monthly_subs = subscription_repo.monthly_total(session, user_id)
    burn_rate = total_expenses + monthly_subs
    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "monthly_subscriptions": round(monthly_subs, 2),
        "burn_rate": round(burn_rate, 2),
        "net": round(total_income - burn_rate, 2),
    }


def get_by_category(session: Session, user_id: int) -> list[dict]:
    return expense_repo.category_totals(session, user_id)


def get_monthly_trend(session: Session, user_id: int) -> list[dict]:
    return expense_repo.monthly_totals(session, user_id)