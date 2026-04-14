from sqlmodel import Session, select, func
from typing import Optional
from datetime import date
from app.models.all_models import Subscription, CategoryEnum, FrequencyEnum


def get_all(session: Session, user_id: int) -> list[Subscription]:
    return list(session.exec(select(Subscription).where(Subscription.user_id == user_id)).all())


def get_by_id(session: Session, sub_id: int) -> Optional[Subscription]:
    return session.get(Subscription, sub_id)


def create(session: Session, user_id: int, name: str, amount: float,
           frequency: FrequencyEnum, next_billing_date: Optional[date],
           category: CategoryEnum, is_active: bool) -> Subscription:
    s = Subscription(name=name, amount=amount, frequency=frequency,
                     next_billing_date=next_billing_date, category=category,
                     is_active=is_active, user_id=user_id)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


def update(session: Session, sub: Subscription, **kwargs) -> Subscription:
    for k, v in kwargs.items():
        if v is not None:
            setattr(sub, k, v)
    session.add(sub)
    session.commit()
    session.refresh(sub)
    return sub


def delete(session: Session, sub: Subscription) -> None:
    session.delete(sub)
    session.commit()


def monthly_total(session: Session, user_id: int) -> float:
    r = session.exec(
        select(func.sum(Subscription.amount)).where(
            Subscription.user_id == user_id,
            Subscription.is_active == True,  # noqa: E712
            Subscription.frequency == FrequencyEnum.monthly,
        )
    ).first()
    return float(r or 0)