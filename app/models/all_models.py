from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from enum import Enum


class CategoryEnum(str, Enum):
    food = "food"
    transport = "transport"
    utilities = "utilities"
    entertainment = "entertainment"
    healthcare = "healthcare"
    shopping = "shopping"
    other = "other"


class FrequencyEnum(str, Enum):
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str
    role: str = Field(default="user")

    expenses: List["Expense"] = Relationship(back_populates="user")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    incomes: List["Income"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")


class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    category: CategoryEnum = CategoryEnum.other
    expense_date: date = Field(default_factory=date.today)  # ← was "date"
    notes: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="expenses")


class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    amount: float
    frequency: FrequencyEnum = FrequencyEnum.monthly
    next_billing_date: Optional[date] = None
    category: CategoryEnum = CategoryEnum.other
    is_active: bool = True
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="subscriptions")


class Income(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    amount: float
    income_date: date = Field(default_factory=date.today)  # ← was "date"
    is_recurring: bool = False
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="incomes")


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: CategoryEnum
    limit_amount: float
    month: int
    year: int
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="budgets")