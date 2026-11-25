from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base.response_schemas import SuccessfulResponse


class DescriptionSchema(BaseModel):
    full: Optional[str] | None = None
    preview: Optional[str] | None = None


class ImageSchema(BaseModel):
    main: Optional[str] | None = None
    preview: Optional[str] | None = None
    cover: Optional[str] | None = None
    icon: Optional[str] | None = None
    emoji: Optional[str] | None = None


class CategorySchema(BaseModel):
    title: Optional[str] | None = None
    value: Optional[str] | None = None


class SalesModelSchema(BaseModel):
    title: Optional[str] | None = None
    value: Optional[str] | None = None


class ProductSchema(BaseModel):
    status: str | None = None
    created_date: datetime | None = None
    modified_date: datetime | None = None
    product_code: Optional[str] = None
    title: str | None = None
    description: DescriptionSchema
    image: ImageSchema
    categories: List[CategorySchema]
    sales_models: List[SalesModelSchema]
    stage: str | None = None
    product_id: UUID | None = None
    product_type: str | None = None
    owner_account_id: UUID | None = None
    ownership: str | None = None


class ResponseProductSchema(SuccessfulResponse):
    data: List[ProductSchema]


class ProductListSchema(SuccessfulResponse):
    data: List[ProductSchema]
