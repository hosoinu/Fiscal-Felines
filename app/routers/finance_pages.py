from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.services import expense_service, income_service, subscription_service, budget_service
from app.models.all_models import CategoryEnum
from datetime import date

# These are added to the main router in __init__.py
from . import router, templates


@router.get("/expenses", response_class=HTMLResponse)
async def expenses_view(request: Request, user: AuthDep, db: SessionDep):
    expenses = expense_service.get_expenses(db, user.id)
    categories = [c.value for c in CategoryEnum]
    return templates.TemplateResponse(request=request, name="expenses.html", context={
        "user": user, "expenses": expenses, "categories": categories
    })


@router.get("/income", response_class=HTMLResponse)
async def income_view(request: Request, user: AuthDep, db: SessionDep):
    incomes = income_service.get_income(db, user.id)
    return templates.TemplateResponse(request=request, name="income.html", context={
        "user": user, "incomes": incomes
    })


@router.get("/subscriptions", response_class=HTMLResponse)
async def subscriptions_view(request: Request, user: AuthDep, db: SessionDep):
    subs = subscription_service.get_subscriptions(db, user.id)
    categories = [c.value for c in CategoryEnum]
    return templates.TemplateResponse(request=request, name="subscriptions.html", context={
        "user": user, "subs": subs, "categories": categories
    })


@router.get("/budget", response_class=HTMLResponse)
async def budget_view(request: Request, user: AuthDep, db: SessionDep):
    status_list = budget_service.get_budget_status(db, user.id)
    budgets = budget_service.get_budgets(db, user.id)
    categories = [c.value for c in CategoryEnum]
    return templates.TemplateResponse(request=request, name="budget.html", context={
        "user": user, "status_list": status_list, "budgets": budgets, "categories": categories, "now_month": date.today().month, "now_year": date.today().year
    })