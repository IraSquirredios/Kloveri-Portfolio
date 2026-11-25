from typing import Annotated
from fastapi import Query, Depends


class PaginationParams:
    def __init__(
        self,
        page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
        per_page: Annotated[int, Query(ge=1, le=50, description="Количество записей на странице")] = 20,
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page
        self.limit = per_page