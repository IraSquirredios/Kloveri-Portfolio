from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.schemas.auth_schemas import Authentication_Schema

router = APIRouter(tags=["authentication"])

@router.post("/sign-in/")
async def sign_in(user: Authentication_Schema):
    "Демонстрационный метод, где можно принять оба поля username, password и переход на стр продуктов"
    username = user.username
    password = user.password

    return RedirectResponse(url="/products", status_code=303)
