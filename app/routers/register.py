from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form
from app.dependencies import SessionDep
from app.services.auth_service import AuthService
from app.utilities.flash import flash
from app.utilities.security import encrypt_password, create_access_token
from . import router, templates


@router.get("/register", response_class=HTMLResponse)
async def register_view(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@router.post("/register", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def signup_user(
    request: Request,
    db: SessionDep,
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
):
    try:
        AuthService.signup(db, username, password, encrypt_password, create_access_token)
        flash(request, "Registration completed! Sign in now!")
        return RedirectResponse(url=request.url_for("login_view"), status_code=status.HTTP_303_SEE_OTHER)
    except Exception:
        flash(request, "Username or email already exists", "danger")
        return RedirectResponse(url=request.url_for("register_view"), status_code=status.HTTP_303_SEE_OTHER)