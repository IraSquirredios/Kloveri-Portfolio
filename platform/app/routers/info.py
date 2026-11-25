from app.libs.auth import validate_permissions
from app.libs.nestorlog import nestor, nlog
from app.schemas.base.info_schemas import Info
from fastapi import APIRouter, Request

router = APIRouter(prefix="/info", tags=["Info"])


@router.get("", response_model=Info, include_in_schema=False)
@nlog
@validate_permissions
async def get_info(request: Request):
    return Info()
