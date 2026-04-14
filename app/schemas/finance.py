from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.all_models import CategoryEnum, FrequencyEnum


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: CategoryEnum = CategoryEnum.other
    expense_date: Optional[date] = None   # ← renamed
    notes: Optional[str] = None


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[CategoryEnum] = None
    expense_date: Optional[date] = None   # ← renamed
    notes: Optional[str] = None


class ExpenseRead(BaseModel):
    id: int
    title: str
    amount: float
    category: CategoryEnum
    expense_date: date                    # ← renamed
    notes: Optional[str]
    user_id: int
    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    name: str
    amount: float
    frequency: FrequencyEnum = FrequencyEnum.monthly
    next_billing_date: Optional[date] = None
    category: CategoryEnum = CategoryEnum.other
    is_active: bool = True


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    frequency: Optional[FrequencyEnum] = None
    next_billing_date: Optional[date] = None
    category: Optional[CategoryEnum] = None
    is_active: Optional[bool] = None


class SubscriptionRead(BaseModel):
    id: int
    name: str
    amount: float
    frequency: FrequencyEnum
    next_billing_date: Optional[date]
    category: CategoryEnum
    is_active: bool
    user_id: int
    class Config:
        from_attributes = True


class IncomeCreate(BaseModel):
    source: str
    amount: float
    income_date: Optional[date] = None   # ← renamed
    is_recurring: bool = False


class IncomeUpdate(BaseModel):
    source: Optional[str] = None
    amount: Optional[float] = None
    income_date: Optional[date] = None   # ← renamed
    is_recurring: Optional[bool] = None


class IncomeRead(BaseModel):
    id: int
    source: str
    amount: float
    income_date: date                    # ← renamed
    is_recurring: bool
    user_id: int
    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category: CategoryEnum
    limit_amount: float
    month: int
    year: int


class BudgetUpdate(BaseModel):
    limit_amount: Optional[float] = None
    month: Optional[int] = None
    year: Optional[int] = None


class BudgetRead(BaseModel):
    id: int
    category: CategoryEnum
    limit_amount: float
    month: int
    year: int
    user_id: int
    class Config:
        from_attributes = True


class BudgetStatus(BaseModel):
    id: int
    category: CategoryEnum
    limit_amount: float
    spent: float
    remaining: float
    over_budget: bool