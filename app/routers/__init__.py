from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.utilities.flash import get_flashed_messages
from jinja2 import Environment, FileSystemLoader
from app.config import get_settings

template_env = Environment(loader=FileSystemLoader("app/templates"))
template_env.globals['get_flashed_messages'] = get_flashed_messages
templates = Jinja2Templates(env=template_env)
static_files = StaticFiles(directory="app/static")

router = APIRouter(
    tags=["Jinja Based Endpoints"],
    include_in_schema=get_settings().env.lower() in ["dev", "development"]
)
api_router = APIRouter(tags=["API Endpoints"], prefix="/api")

# Existing template routers
from . import index, login, register, admin_home, user_home, users, logout, finance_pages

# New finance API routers
from .expenses import router as expenses_router
from .subscriptions import router as subscriptions_router
from .income import router as income_router
from .budgets import router as budgets_router
from .reports import router as reports_router

api_router.include_router(expenses_router)
api_router.include_router(subscriptions_router)
api_router.include_router(income_router)
api_router.include_router(budgets_router)
api_router.include_router(reports_router)