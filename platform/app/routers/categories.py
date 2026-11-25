from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Request, Depends, Header

from app.schemas.base.pagination_schemas import PaginationParams
from app.services.base.utils import HeaderAlias
from app.services.category_service import get_categories_by_project_id

router = APIRouter(tags=["categories"])


@router.get("/categories/", status_code=status.HTTP_200_OK,
            summary="Получить категории")
# @nlog
# @validate_permissions
async def get_categories(
        request: Request,
        pagination: Annotated[PaginationParams, Depends()],
        project_id: Annotated[UUID, Header(alias=HeaderAlias.PROJECT_ID)]
):
    result = await get_categories_by_project_id(
        request=request,
        project_id=project_id,
        # limit=pagination.limit,
        # offset=pagination.offset
    )
    # response = ProductListSchema(
    #     detail=ResponseDetail(code="OK", message="Продукты получены"),
    #     data=result,
    #     info=ResponseInfo(count=0, total=len(result), page=pagination.page, page_size=pagination.per_page)  # TODO
    # )
    return result
