from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Request, Header, Depends, status
from app.services.product_service import get_products_entries_by_project_id, get_product_by_id
from app.libs.auth import validate_permissions
from app.libs.nestorlog import nlog
from app.schemas.base.pagination_schemas import PaginationParams
from app.services.base.utils import HeaderAlias
from app.exceptions.main_exceptions import NotImplementedException
from app.schemas.products_schemas import ProductListSchema, ProductSchema, ResponseProductSchema
from app.schemas.base.response_schemas import ResponseDetail, ResponseInfo

router = APIRouter(tags=["products"])


@router.get("/products/", response_model=ProductListSchema, status_code=status.HTTP_200_OK, summary="Получить продукты")
# @nlog
# @validate_permissions
async def get_all_products(
        request: Request,
        pagination: Annotated[PaginationParams, Depends()],
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)]
) -> ProductListSchema:
    result = await get_products_entries_by_project_id(
        request=request,
        project_id=project_id,
        limit=pagination.limit,
        offset=pagination.offset
    )
    response = ProductListSchema(
        detail=ResponseDetail(code="OK", message="Продукты получены"),
        data=result,
        info=ResponseInfo(count=0, total=len(result), page=pagination.page, page_size=pagination.per_page)  # TODO
    )
    return response


@router.get("/product/{product_id}/", response_model=ResponseProductSchema, status_code=status.HTTP_200_OK,
            summary="Получить продукт по id")
# @nlog
# @validate_permissions
async def get_product_id(
        request: Request,
        product_id: UUID,
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)]
) -> ResponseProductSchema:
    result = await get_product_by_id(
        request=request,
        project_id=project_id,
        product_id=product_id
    )
    response = ResponseProductSchema(
        detail=ResponseDetail(code="OK", message="Продукт получен"),
        data=result,
        info=ResponseInfo(count=1, total=1, page=1, page_size=1)
    )
    return response


@router.post('/product/', status_code=status.HTTP_201_CREATED)
@nlog
# @validate_permissions
async def create_product(
        request: Request,
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)],
        data: dict
):
    raise NotImplementedException


@router.patch('/product/{product_id}/', status_code=status.HTTP_200_OK)
@nlog
# @validate_permissions
async def update_product(
        request: Request,
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)],
        product_id: UUID,
        data: dict
):
    raise NotImplementedException


@router.delete('/product/{product_id}/', status_code=status.HTTP_200_OK)
@nlog
# @validate_permissions
async def delete_product(
        request: Request,
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)],
        product_id: UUID,
        data: dict
):
    raise NotImplementedException
