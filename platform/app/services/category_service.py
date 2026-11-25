from urllib.request import Request
from uuid import UUID
from fastapi import status

from app.services.base.service.api_interaction import interact_with_api
from app.services.base.utils import HeaderAlias, Method, Handle
from app.config import settings
from app.exceptions.main_exceptions import ServiceException
from app.exceptions.sub_exceptions.not_found_exceptions import ProfilesNotFoundException


async def get_categories_by_project_id(
        request: Request,
        project_id: UUID,
):
    headers = {HeaderAlias.PROJECT_ID: str(project_id)}

    params = {
        "project_id": project_id
    }
    try:
        categories = await interact_with_api(
            request=request,
            method=Method.GET,
            api_url=settings.DIRECTORY_API_URL,
            handle=Handle.DIRECTORY.resolve(directory="product"),
            headers=headers,
            params=params
        )
        return categories.get('data')
    except ServiceException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise ProfilesNotFoundException
        raise e
