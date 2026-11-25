from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Request, Header, Depends, status

from app.config import settings

from app.libs.auth import validate_permissions
from app.libs.auth.token import token_info
from app.libs.nestorlog import nlog, nestor

from app.exceptions.main_exceptions import NotImplementedException

from app.schemas.base.response_schemas import SuccessfulResponse, ResponseDetail, ResponseInfo
from app.schemas.base.pagination_schemas import PaginationParams

from app.services.base.utils import HeaderAlias


router = APIRouter(tags=["Методы сервиса"])


@router.get("/examples", response_model=SuccessfulResponse, response_model_exclude_none=True, summary='Получить примеры вывода')
@nlog
@validate_permissions
async def get_example_output(
    request: Request,
    project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)],
    pagination: Annotated[PaginationParams, Depends()],
):
    raise NotImplementedException

    output = [ { "limit": pagination.limit, "offset": pagination.offset } ]

    # response = SuccessfulResponse(
    #     detail=ResponseDetail(
    #         code='OK',
    #         message='Запрос успешно обработан'
    #     ),
    #     data=output,
    #     info=ResponseInfo(
    #         total=result.get('total'),
    #         count=result.get('count'),
    #         page=pagination.page,
    #         page_size=pagination.per_page
    #     ),
    # )
    # return response


@router.post('/example/', status_code=status.HTTP_201_CREATED, response_model=SuccessfulResponse, response_model_exclude_none=True, summary='Создать пример')
@nlog
@validate_permissions
async def create_example(
    request: Request,
    project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)],
    data: dict
) -> SuccessfulResponse:
    raise NotImplementedException

    return SuccessfulResponse(
        detail=ResponseDetail(
            code='OK',
            message='Пример создан'
        ),
        info=ResponseInfo(),
    )
