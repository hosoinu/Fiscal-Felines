from fastapi import APIRouter
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.schemas.finance import SubscriptionCreate, SubscriptionUpdate, SubscriptionRead
from app.services import subscription_service

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("/", response_model=list[SubscriptionRead])
def list_subscriptions(current_user: AuthDep, db: SessionDep):
    return subscription_service.get_subscriptions(db, current_user.id)


@router.post("/", response_model=SubscriptionRead, status_code=201)
def add_subscription(data: SubscriptionCreate, current_user: AuthDep, db: SessionDep):
    return subscription_service.create_subscription(db, current_user.id, data)


@router.put("/{sub_id}", response_model=SubscriptionRead)
def edit_subscription(sub_id: int, data: SubscriptionUpdate, current_user: AuthDep, db: SessionDep):
    return subscription_service.update_subscription(db, sub_id, current_user.id, data)


@router.delete("/{sub_id}")
def remove_subscription(sub_id: int, current_user: AuthDep, db: SessionDep):
    subscription_service.delete_subscription(db, sub_id, current_user.id)
    return {"message": "Deleted"}