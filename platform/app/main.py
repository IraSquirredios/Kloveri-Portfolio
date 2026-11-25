from contextlib import asynccontextmanager

from app.config import settings
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from app.libs.auth import init_auth
from app.libs.nestorlog import init_logger
from app.libs.session_context import SessionContextMiddleware
from app.libs.uhttp import HTTPClient
from app.routers.auth_demo import router as auth_router
from app.routers.products import router as product_router
from app.routers.categories import router as categories_router
from app.routers.info import router as info_router
from app.routers.service_methods import router as service_router
from app.schemas.base.response_schemas import ExceptionDetail, ResponseDetail
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение HTTP-клиента
    app.requests_client = HTTPClient(
        timeout=settings.UHTTP_TIMEOUT,
        resolve_ip=settings.UHTTP_RESOLVE_IP,
        log_dns=settings.UHTTP_LOG_DNS,
        log_responses=settings.UHTTP_LOG_RESPONSE,
        verify_ssl=settings.UHTTP_VERIFY_SSL,
    )
    print("STARTUP: HTTP client initialized.")

    # Инициализация логгера
    init_logger(
        service_name=settings.SERVICE_NAME,
        settings=settings
    )

    #   Подключение авторизации
    init_auth(app)

    try:
        yield
    finally:
        # При завершении закрываем клиент
        await app.requests_client.close()


app = FastAPI(
    title="Портфолио",
    lifespan=lifespan,
    version=settings.VERSION
)

app.add_middleware(SessionContextMiddleware)

# app.include_router(info_router)
# app.include_router(service_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(categories_router)

origins = settings.ALLOWED_HOSTS.split()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_type = exc.errors()[0].get('type')
    location = exc.errors()[0].get('loc')
    message = exc.errors()[0].get('msg')
    request_input = exc.errors()[0].get('input')
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ExceptionDetail(
                detail=ResponseDetail(
                    code="BAD_REQUEST",
                    message=f'Type: {error_type}, location: {location}. {message}. Input: {request_input}'
                )
            )
        )
    )
