from urllib.request import Request
from uuid import UUID
from fastapi import status

from app.services.base.service.api_interaction import interact_with_api
from app.services.base.utils import HeaderAlias, Method, Handle
from app.config import settings
from app.exceptions.main_exceptions import ServiceException
from app.exceptions.sub_exceptions.not_found_exceptions import ProfilesNotFoundException


async def get_products_entries_by_project_id(
        request: Request,
        project_id: UUID,
        limit: int,
        offset: int | None
):
    headers = {HeaderAlias.PROJECT_ID: str(project_id)}

    params = {
        "project_id": project_id,
        "limit": min(limit, 200),
        "offset": offset
    }

    try:
        products = await interact_with_api(
            request=request,
            method=Method.GET,
            api_url=settings.PRODUCT_API_URL,
            handle=Handle.PRODUCTS.resolve(),
            headers=headers,
            params=params
        )
        return products.get('data')
    except ServiceException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise ProfilesNotFoundException
        raise e


async def get_product_by_id(
        request: Request,
        project_id: UUID,
        product_id: UUID
):
    headers = {HeaderAlias.PROJECT_ID: str(project_id)}

    params = {
        "project_id": project_id
    }
    try:
        product = await interact_with_api(
            request=request,
            method=Method.GET,
            api_url=settings.PRODUCT_API_URL,
            handle=Handle.PRODUCT.resolve(product_id=product_id),
            headers=headers,
            params=params
        )
        return product.get('data')
    except ServiceException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise ProfilesNotFoundException
        raise e
