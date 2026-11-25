from uuid import UUID

from pydantic import BaseModel

from app.schemas.base.base_schemas import RegistryObject


class ProjectRegistryData(BaseModel):
    message: str | None = None


class ProjectRegistryObject(RegistryObject):
    data: ProjectRegistryData | None = None


class ProjectModel(BaseModel):
    project_id: UUID
    project_type: str
    project_name: str
    message: str


class ProfileModel(BaseModel):
    profile_id: UUID
    first_name: str
    last_name: str
    middle_name: str
    project_id: UUID


class CombinedOutput(BaseModel):
    profile_id: UUID
    project_id: UUID
    message: str
