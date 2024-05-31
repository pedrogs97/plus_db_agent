"""Base service class that will be inherited by all other services"""

from typing import List, Type, get_type_hints

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page, Params, paginate
from pydantic import ValidationError

from plus_db_agent.controller import GenericController
from plus_db_agent.filters import BaseFilter, PaginationFilter
from plus_db_agent.logger import logger
from plus_db_agent.models import BaseModel, T, UserModel
from plus_db_agent.schemas import BaseSchema


class GenericService:
    """Base service class that will be inherited by all other services"""

    model: Type[T]
    controller = GenericController()
    module_name = "base"
    serializer = Type[BaseSchema]

    async def serializer_obj(self, obj: T, serializer: BaseSchema) -> BaseSchema:
        data = obj.__dict__
        hints = get_type_hints(serializer)

        for field_name, field_type in hints.items():
            if isinstance(field_type, type) and issubclass(field_type, BaseSchema):
                # Se o campo é uma submodel está presente nos dados
                if field_name in data and isinstance(data[field_name], BaseModel):
                    try:
                        # Recursivamente cria uma serailzier da submodel
                        data[field_name] = await self.serializer_obj(
                            data[field_name], field_type
                        )
                    except ValidationError as e:
                        logger.warning(
                            f"Erro de validação no campo {field_name}: %s", e
                        )
                        raise

        try:
            # Cria um serializer da model principal a partir do dicionário
            instance = serializer(**data)
        except ValidationError as e:
            logger.warning("Erro de validação no modelo: %s", e)
            raise

        return instance

    async def serializer_list(self, objs: List[T]) -> List[BaseSchema]:
        return [await self.serializer_obj(obj, self.serializer) for obj in objs]

    async def get_obj_or_404(self, pk: int) -> T:
        """Get an object by its id or raise a 404 error"""
        obj = await self.controller.get_obj_or_none(pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return await self.serializer_obj(obj, self.serializer)

    async def paginated_list(
        self, list_filters: BaseFilter, page_filter: PaginationFilter
    ) -> Page[T]:
        """List paginated objects"""
        user_list = await list_filters.filter(self.model.filter(deleted=False))
        user_list = await self.serializer_list(user_list.all())
        paginated = paginate(
            user_list,
            params=Params(page=page_filter.page, size=page_filter.size),
        )
        return paginated

    async def list(self, **filters) -> List[BaseSchema]:
        """List objects"""
        list_objs = await self.controller.list(**filters)
        return await self.serializer_list(list_objs)

    async def add(self, record: dict, authenticated_user: UserModel) -> T:
        """Add an object"""
        obj_created: T = await self.controller.add(record, authenticated_user)
        return self.serializer_obj(obj_created, self.serializer)

    async def update(self, record: dict, pk: int, authenticated_user: UserModel) -> T:
        """Update an object"""
        obj_updated = await self.controller.update(record, pk, authenticated_user)
        if not obj_updated:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return self.serializer_obj(obj_updated, self.serializer)

    async def delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Delete an object"""
        obj: T = await self.controller.get_obj_or_none(pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await self.controller.delete(obj.id, authenticated_user)

    async def soft_delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Soft delete an object"""
        await self.update({"deleted": True}, pk, authenticated_user)

    async def get_by_field(self, field: str, value: str) -> T:
        """Get an object by a field"""
        obj = await self.controller.get_by_field(field, value)
        if not obj:
            raise HTTPException(
                detail={"field": field, "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return await self.serializer_obj(obj, self.serializer)
