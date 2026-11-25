from uuid import UUID
from datetime import datetime

from fastapi import Request

from app.config import settings
from app.schemas.base.base_schemas import ItemStatus
from app.services.base.registry.registry_interaction import interact_with_registry, make_meta, registry_make_search_params
from app.services.base.utils import Method, Timeout, get_project, get_account, get_user
from app.exceptions.main_exceptions import NotFoundException, DeletedException
from app.exceptions.sub_exceptions.not_found_exceptions import RegistryObjectDeactivatedException

__version__ = "1.0.0"


class ItemsService:
    def __init__(
        self,
        single_name: str,
        plural_name: str,
        base_registry_url: str = None,
    ):
        self.base_registry_url = base_registry_url or settings.SERVICE_REGISTRY_URL
        self.single_endpoint = single_name
        self.plural_endpoint = plural_name

    # Создаёт новый объект в реестре
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта (опционально, если не указан - генерируется)
    #   object_type: str - тип объекта (например, "book", "person")
    #   object_code: str - уникальный код объекта (опционально)
    #   object_item: UUID - ID родительского объекта (опционально)
    #   data: dict - произвольные данные объекта (опционально)
    #   meta: dict - метаданные объекта (опционально)
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - созданный объект
    async def create(
        self,
        request: Request,
        object_id: UUID = None,
        object_type: str = None,
        object_code: str = None,
        object_item: UUID = None,
        data: dict = None,
        meta: dict = None,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        payload = {}
        if object_id is not None:
            payload["id"] = str(object_id)
        if object_type is not None:
            payload["object_type"] = object_type
        if object_code is not None:
            payload["object_code"] = object_code
        if object_item is not None:
            payload["object_item"] = str(object_item)
        if data is not None:
            payload["data"] = data
        if meta is not None:
            payload["meta"] = meta

        # Всегда подставляем DEFAULT при отсутствии явных значений
        payload["project_id"] = get_project(project_id)
        payload["account_id"] = get_account(account_id)
        payload["user_id"] = get_user(user_id)

        return await interact_with_registry(
            request=request,
            method=Method.POST,
            registry_url=self.base_registry_url,
            registry_name=self.single_endpoint,
            data=payload,
            timeout=timeout,
        )

    # Получает объект по ID с проверкой принадлежности к проекту/аккаунту/пользователю
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   active_records: bool - возвращать только активные записи (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - объект
    async def get(
        self,
        request: Request,
        object_id: UUID,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        active_records: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        result = await interact_with_registry(
            request=request,
            method=Method.GET,
            registry_url=self.base_registry_url,
            registry_name=self.single_endpoint,
            _id=object_id,
            active_records=active_records,
            timeout=timeout,
        )

        # Проверка project_id
        if project_id is not None:
            if get_project(result.get("project_id")) != get_project(project_id):
                raise NotFoundException(f"Объект с ID {object_id} не найден")

        # Проверка account_id
        if check_account and get_account(result.get("account_id")) != get_account(account_id):
            raise NotFoundException(f"Объект с ID {object_id} не найден")

        # Проверка user_id
        if check_user and get_user(result.get("user_id")) != get_user(user_id):
            raise NotFoundException(f"Объект с ID {object_id} не найден")

        return result

    # Полностью обновляет объект (PUT)
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   data: dict - полные данные объекта для обновления
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - обновлённый объект
    async def update(
        self,
        request: Request,
        object_id: UUID,
        data: dict,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        # Проверяем существование и права доступа через get
        await self.get(
            request=request,
            object_id=object_id,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=True,
            timeout=timeout,
        )

        return await interact_with_registry(
            request=request,
            method=Method.PUT,
            registry_url=self.base_registry_url,
            registry_name=self.single_endpoint,
            _id=object_id,
            data=data,
            timeout=timeout,
        )

    # Частично обновляет объект (PATCH)
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   object_code: str - уникальный код объекта (опционально)
    #   object_type: str - тип объекта (опционально)
    #   object_item: UUID - ID родительского объекта (опционально)
    #   data: dict - произвольные данные для обновления (опционально)
    #   meta: dict - метаданные для обновления (опционально)
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - обновлённый объект
    async def patch(
        self,
        request: Request,
        object_id: UUID,
        object_code: str = None,
        object_type: str = None,
        object_item: UUID = None,
        data: dict = None,
        meta: dict = None,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        # Проверяем существование и права доступа через get
        await self.get(
            request=request,
            object_id=object_id,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=True,
            timeout=timeout,
        )

        patch_data = {}

        # Поля верхнего уровня
        if object_code is not None:
            patch_data["object_code"] = object_code
        if object_type is not None:
            patch_data["object_type"] = object_type
        if object_item is not None:
            patch_data["object_item"] = str(object_item)

        # Вложенные поля
        if data is not None:
            patch_data["data"] = data
        if meta is not None:
            patch_data["meta"] = meta

        return await interact_with_registry(
            request=request,
            method=Method.PATCH,
            registry_url=self.base_registry_url,
            registry_name=self.single_endpoint,
            _id=object_id,
            data=patch_data,
            timeout=timeout,
        )


    # Деактивирует объект (мягкое удаление)
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   change_code: bool - заменять object_code на "старый_код:id" (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - объект с обновлённым статусом
    async def delete(
        self,
        request: Request,
        object_id: UUID,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        change_code: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        return await self.set_status(
            request, object_id, ItemStatus.HIDDEN,
            project_id, account_id, user_id,
            check_account, check_user, timeout,
            change_code=change_code,
        )


    # Устанавливает статус объекта
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   status: str - новый статус ("active" или "inactive")
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    #   change_code: bool - изменять object_code при смене статуса:
    #                       - при деактивации: добавляет ":id" к object_code
    #                       - при активации: удаляет ":id" из конца object_code
    # Выходные параметры:
    #   dict - объект с обновлённым статусом
    # Исключения:
    #   DeletedException - если объект уже удалён
    async def set_status(
        self,
        request: Request,
        object_id: UUID,
        status: str,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
        change_code: bool = False,
    ) -> dict:
        current = await self.get(
            request=request,
            object_id=object_id,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=False,
            timeout=timeout,
        )

        # Если объект уже в нужном статусе
        current_status = current.get("meta", {}).get("status")
        if current_status == status:
            if status == ItemStatus.HIDDEN:
                raise DeletedException()
            return current

        updated_meta = make_meta(existing_meta=current.get("meta"), status=status)
        patch_data = {"meta": updated_meta}

        # Изменение object_code при деактивации
        if change_code and status == ItemStatus.HIDDEN:
            old_code = current.get("object_code")
            new_code = f"{old_code}:{object_id}" if old_code else str(object_id)
            patch_data["object_code"] = new_code

        # Восстановление object_code при активации
        if change_code and status == ItemStatus.ACTIVE:
            old_code = current.get("object_code", "")
            parts = old_code.rsplit(":", 1)
            if len(parts) == 2 and parts[1] == str(object_id):
                patch_data["object_code"] = parts[0]
            else:
                patch_data["object_code"] = old_code

        try:
            return await interact_with_registry(
                request=request,
                method=Method.PATCH,
                registry_url=self.base_registry_url,
                registry_name=self.single_endpoint,
                _id=object_id,
                data=patch_data,
                timeout=timeout,
            )
        except RegistryObjectDeactivatedException:
            # Если при попытке обновления выяснилось, что объект удалён
            raise DeletedException()

    # Устанавливает битовые флаги объекта
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   flags: int - новое значение флагов
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - объект с обновлёнными флагами
    async def set_flags(
        self,
        request: Request,
        object_id: UUID,
        flags: int,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        current = await self.get(
            request=request,
            object_id=object_id,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=False,
            timeout=timeout,
        )
        updated_meta = make_meta(existing_meta=current.get("meta"), flags=flags)
        return await self.patch(
            request=request,
            object_id=object_id,
            meta=updated_meta,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            timeout=timeout,
        )

    # Активирует объект (устанавливает статус "active")
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_id: UUID - ID объекта
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   restore_code: bool - восстанавливать object_code (удалять ":id" из конца) (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - объект с обновлённым статусом
    async def activate(
        self,
        request: Request,
        object_id: UUID,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        restore_code: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        return await self.set_status(
            request, object_id, ItemStatus.ACTIVE,
            project_id, account_id, user_id,
            check_account, check_user, timeout,
            change_code=restore_code,
        )


    # Получает список объектов с фильтрацией, пагинацией, сортировкой и фильтрацией по датам
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   project_id: UUID - ID проекта
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   ids: list[UUID] - список ID объектов для фильтрации (опционально)
    #   check_account: bool - если True, ищем точное совпадение account_id,
    #                        если False - ищем переданный account_id или DEFAULT_ACCOUNT
    #   ignore_account: bool - если True, то игнорируем поиск по аккаунту
    #   check_user: bool - если True, добавляем фильтр по user_id,
    #                     если False - не добавляем фильтр по user_id
    #   offset: int - количество пропускаемых записей (опционально)
    #   limit: int - количество возвращаемых записей (опционально)
    #   sort_by: str - поле для сортировки (например, "created_date", "data__title")
    #   order_by: str - направление сортировки ("asc" или "desc")
    #   modified_after: datetime - начало диапазона по modified_date (опционально)
    #   modified_before: datetime - окончание диапазона по modified_date (опционально)
    #   created_after: datetime - начало диапазона по created_date (опционально)
    #   created_before: datetime - окончание диапазона по created_date (опционально)
    #   active_records: bool - возвращать только активные записи (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.MEDIUM)
    #   **filters: dict - произвольные параметры фильтрации
    # Выходные параметры:
    #   dict - объект с полями count (текущее количество), total (общее количество),
    #          next, previous, results
    async def items(
        self,
        request: Request,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        ids: list[UUID] = None,
        check_account: bool = True,
        ignore_account: bool = False,
        check_user: bool = True,
        offset: int = None,
        limit: int = None,
        sort_by: str = None,
        order_by: str = None,
        modified_after: datetime = None,
        modified_before: datetime = None,
        created_after: datetime = None,
        created_before: datetime = None,
        active_records: bool = True,
        timeout: float | Timeout = Timeout.MEDIUM,
        **filters,
    ) -> dict:
        params = {k: v for k, v in filters.items() if v is not None}

        # Фильтрация по списку ID
        if ids is not None:
            params["id"] = ",".join(str(id_) for id_ in ids)

        # Пагинация
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        # Сортировка и даты
        params = registry_make_search_params(
            params,
            modified_after=modified_after,
            modified_before=modified_before,
            created_after=created_after,
            created_before=created_before,
            sort_by=sort_by,
            order_by=order_by,
        )

        # project_id
        params["project_id"] = get_project(project_id)

        # account_id
        if check_account:
            params["account_id"] = get_account(account_id)
        else:
            if account_id is not None:
                params["account_id"] = f"{account_id},{get_account(None)}"
            else:
                if not ignore_account:
                    params["account_id"] = get_account(None)

        # user_id
        if check_user:
            params["user_id"] = get_user(user_id)

        result = await interact_with_registry(
            request=request,
            method=Method.GET,
            registry_url=self.base_registry_url,
            registry_name=self.plural_endpoint,
            params=params,
            active_records=active_records,
            timeout=timeout,
        )

        # Приводим к единому формату словаря
        if isinstance(result, list):
            return {
                "count": len(result),
                "total": len(result),
                "next": None,
                "previous": None,
                "results": result,
            }
        else:
            if "total" not in result:
                result["total"] = result.get("count", 0)
                result["count"] = len(result.get("results", []))
            return result

    # Проверяет существование объекта и возвращает его ID
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.FAST)
    #   **filters: dict - произвольные параметры фильтрации
    # Выходные параметры:
    #   UUID | None - ID найденного объекта, если существует, иначе None
    async def exists_or_get_id(
        self,
        request: Request,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.FAST,
        **filters,
    ) -> UUID | None:
        params = {k: v for k, v in filters.items() if v is not None}
        params["limit"] = 1

        response = await self.items(
            request=request,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=True,
            timeout=timeout,
            **params,
        )

        results = response.get("results", [])
        if results:
            return results[0]["id"]
        return None

    # Проверяет существование объекта
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.FAST)
    #   **filters: dict - произвольные параметры фильтрации
    # Выходные параметры:
    #   bool - True если хотя бы один объект найден, иначе False
    async def exists(
        self,
        request: Request,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.FAST,
        **filters,
    ) -> bool:
        result = await self.exists_or_get_id(
            request=request,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            timeout=timeout,
            **filters,
        )
        return result is not None

    # Возвращает количество объектов, соответствующих фильтрам
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.MEDIUM)
    #   **filters: dict - произвольные параметры фильтрации
    # Выходные параметры:
    #   int - количество объектов, соответствующих фильтрам
    async def count(
        self,
        request: Request,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.MEDIUM,
        **filters,
    ) -> int:
        params = {k: v for k, v in filters.items() if v is not None}
        params["limit"] = 1
        response = await self.items(
            request=request,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            active_records=True,
            timeout=timeout,
            **params,
        )
        return response.get("count", 0)

    # Массовое создание объектов
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   objects: list[dict] - массив объектов для создания
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.LONG)
    # Выходные параметры:
    #   list[dict] - массив созданных объектов
    async def bulk_create(
        self,
        request: Request,
        objects: list[dict],
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        timeout: float | Timeout = Timeout.LONG,
    ) -> list[dict]:
        processed_objects = []
        for obj in objects:
            obj["project_id"] = get_project(obj.get("project_id", project_id))
            obj["account_id"] = get_account(obj.get("account_id", account_id))
            obj["user_id"] = get_user(obj.get("user_id", user_id))
            processed_objects.append(obj)

        return await interact_with_registry(
            request=request,
            method=Method.POST,
            registry_url=self.base_registry_url,
            registry_name=self.plural_endpoint,
            data=processed_objects,
            timeout=timeout,
        )

    # Массовое обновление объектов (PUT)
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   objects: list[dict] - массив объектов для полного обновления
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.LONG)
    # Выходные параметры:
    #   list[dict] - массив обновлённых объектов
    async def bulk_update(
        self,
        request: Request,
        objects: list[dict],
        timeout: float | Timeout = Timeout.LONG,
    ) -> list[dict]:
        return await interact_with_registry(
            request=request,
            method=Method.PUT,
            registry_url=self.base_registry_url,
            registry_name=self.plural_endpoint,
            data=objects,
            timeout=timeout,
        )

    # Массовое частичное обновление объектов (PATCH)
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   objects: list[dict] - массив объектов для частичного обновления
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.LONG)
    # Выходные параметры:
    #   list[dict] - массив обновлённых объектов
    async def bulk_patch(
        self,
        request: Request,
        objects: list[dict],
        timeout: float | Timeout = Timeout.LONG,
    ) -> list[dict]:
        return await interact_with_registry(
            request=request,
            method=Method.PATCH,
            registry_url=self.base_registry_url,
            registry_name=self.plural_endpoint,
            data=objects,
            timeout=timeout,
        )

    # Массовое удаление объектов
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   object_ids: list[UUID] - массив ID объектов для удаления
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.LONG)
    # Выходные параметры:
    #   dict - ответ API с результатом операции
    async def bulk_delete(
        self,
        request: Request,
        object_ids: list[UUID],
        timeout: float | Timeout = Timeout.LONG,
    ) -> dict:
        params = {"id": ",".join(str(id_) for id_ in object_ids)}
        return await interact_with_registry(
            request=request,
            method=Method.DELETE,
            registry_url=self.base_registry_url,
            registry_name=self.plural_endpoint,
            params=params,
            timeout=timeout,
        )

    # Создаёт или обновляет объект по уникальному полю
    # Входные параметры:
    #   request: Request - объект запроса FastAPI
    #   unique_field: str - имя уникального поля (например, "object_code")
    #   unique_value: str | UUID - значение уникального поля
    #   object_id: UUID - ID объекта (опционально)
    #   object_type: str - тип объекта (опционально)
    #   object_code: str - уникальный код объекта (опционально)
    #   object_item: UUID - ID родительского объекта (опционально)
    #   data: dict - произвольные данные объекта (опционально)
    #   meta: dict - метаданные объекта (опционально)
    #   project_id: UUID - ID проекта (опционально)
    #   account_id: UUID - ID аккаунта (опционально)
    #   user_id: UUID - ID пользователя (опционально)
    #   check_account: bool - проверять принадлежность к аккаунту (по умолчанию True)
    #   check_user: bool - проверять принадлежность к пользователю (по умолчанию True)
    #   timeout: float | Timeout - таймаут операции (по умолчанию Timeout.DEFAULT)
    # Выходные параметры:
    #   dict - созданный или обновлённый объект
    async def upsert(
        self,
        request: Request,
        unique_field: str,
        unique_value: str | UUID,
        object_id: UUID = None,
        object_type: str = None,
        object_code: str = None,
        object_item: UUID = None,
        data: dict = None,
        meta: dict = None,
        project_id: UUID = None,
        account_id: UUID = None,
        user_id: UUID = None,
        check_account: bool = True,
        check_user: bool = True,
        timeout: float | Timeout = Timeout.DEFAULT,
    ) -> dict:
        existing_id = await self.exists_or_get_id(
            request=request,
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            check_account=check_account,
            check_user=check_user,
            timeout=timeout,
            **{unique_field: unique_value},
        )

        if existing_id:
            update_data = {}
            if object_id is not None:
                update_data["id"] = str(object_id)
            if object_type is not None:
                update_data["object_type"] = object_type
            if object_code is not None:
                update_data["object_code"] = object_code
            if object_item is not None:
                update_data["object_item"] = str(object_item)
            if data is not None:
                update_data["data"] = data
            if meta is not None:
                update_data["meta"] = meta
            if project_id is not None:
                update_data["project_id"] = str(project_id)
            if account_id is not None:
                update_data["account_id"] = str(account_id)
            if user_id is not None:
                update_data["user_id"] = str(user_id)

            return await self.update(
                request=request,
                object_id=existing_id,
                data=update_data,
                project_id=project_id,
                account_id=account_id,
                user_id=user_id,
                check_account=check_account,
                check_user=check_user,
                timeout=timeout,
            )
        else:
            return await self.create(
                request=request,
                object_id=object_id,
                object_type=object_type,
                object_code=object_code,
                object_item=object_item,
                data=data,
                meta=meta,
                project_id=project_id,
                account_id=account_id,
                user_id=user_id,
                timeout=timeout,
            )