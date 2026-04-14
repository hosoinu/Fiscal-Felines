from sqlmodel import Session
from fastapi import HTTPException, status
from app.repositories import subscription_repo
from app.models.all_models import Subscription
from app.schemas.finance import SubscriptionCreate, SubscriptionUpdate


def get_subscriptions(session: Session, user_id: int) -> list[Subscription]:
    return subscription_repo.get_all(session, user_id)


def create_subscription(session: Session, user_id: int, data: SubscriptionCreate) -> Subscription:
    return subscription_repo.create(
        session=session,
        user_id=user_id,
        name=data.name,
        amount=data.amount,
        frequency=data.frequency,
        next_billing_date=data.next_billing_date,
        category=data.category,
        is_active=data.is_active,
    )


def update_subscription(session: Session, sub_id: int, user_id: int, data: SubscriptionUpdate) -> Subscription:
    s = subscription_repo.get_by_id(session, sub_id)
    if not s or s.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription_repo.update(session, s, **data.model_dump(exclude_unset=True))


def delete_subscription(session: Session, sub_id: int, user_id: int) -> None:
    s = subscription_repo.get_by_id(session, sub_id)
    if not s or s.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    subscription_repo.delete(session, s)