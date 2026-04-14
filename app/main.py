import uvicorn
from fastapi import FastAPI, Request, status
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import get_settings
from contextlib import asynccontextmanager

# Load ALL models first so tables register before anything else touches them
from app.models.all_models import User, Expense, Subscription, Income, Budget  # noqa

# Now safe to import routers
from app.routers import templates, static_files, router, api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import create_db_and_tables, engine
    from sqlmodel import Session, select
    from app.utilities.security import encrypt_password

    create_db_and_tables()

    with Session(engine) as session:
        if not session.exec(select(User).where(User.username == "bob")).first():
            session.add(User(username="bob", password=encrypt_password("bobpass")))
            session.commit()

        if not session.exec(select(User).where(User.username == "aneesa")).first():
            session.add(User(username="aneesa", password=encrypt_password("12345")))
            session.commit()

    yield


app = FastAPI(
    middleware=[
        Middleware(SessionMiddleware, secret_key=get_settings().secret_key)
    ],
    lifespan=lifespan,
)

app.include_router(router)
app.include_router(api_router)
app.mount("/static", static_files, name="static")


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_redirect_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request,
        name="401.html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=get_settings().app_host,
        port=get_settings().app_port,
        reload=get_settings().env.lower() != "production",
    )