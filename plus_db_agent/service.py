"""Base service class that will be inherited by all other services"""

from typing import List, Type, get_type_hints

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from pydantic import ValidationError

from plus_db_agent.config import NOT_FOUND
from plus_db_agent.controller import GenericController
from plus_db_agent.filters import BaseFilter, PaginationFilter
from plus_db_agent.logger import logger
from plus_db_agent.models import BaseModel, UserModel
from plus_db_agent.schemas import BaseSchema


class GenericService:
    """Base service class that will be inherited by all other services"""

    model = BaseModel
    controller = GenericController()
    module_name = "base"
    serializer = Type[BaseSchema]

    async def serializer_obj(self, obj: BaseModel, serializer: BaseSchema) -> dict:
        """Create a serializer object from a model object"""
        data = obj.__dict__.copy()
        hints = get_type_hints(serializer)

        for field_name, field_type in hints.items():
            if (
                isinstance(field_type, type)
                and issubclass(field_type, BaseSchema)
                and hasattr(obj, field_name)
            ):
                # Se o campo é uma submodel está presente nos dados
                await obj.fetch_related(field_name)
                related_obj = getattr(obj, field_name)
                if isinstance(related_obj, BaseModel):
                    try:
                        # Recursivamente cria uma serailzier da submodel
                        data[field_name] = await self.serializer_obj(
                            obj=related_obj, serializer=field_type
                        )
                    except ValidationError as e:
                        logger.warning("Erro de validação no campo %s", field_name)
                        logger.warning("Erro: %s", e)
                        raise

        try:
            # Cria um serializer da model principal a partir do dicionário
            instance = serializer(**data)
        except ValidationError as e:
            logger.warning("Erro de validação no modelo: %s", e)
            raise

        return instance.model_dump(by_alias=True)

    async def serializer_list(self, objs: List[BaseModel]) -> List[dict]:
        """Create a list of serializer objects from a list of model objects"""
        return [
            await self.serializer_obj(obj=obj, serializer=self.serializer)
            for obj in objs
        ]

    async def get_obj_or_404(self, pk: int) -> dict:
        """Get an object by its id or raise a 404 error"""
        obj = await self.controller.get_obj_or_none(pk=pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return await self.serializer_obj(obj=obj, serializer=self.serializer)

    async def paginated_list(
        self,
        list_filters: BaseFilter,
        page_filter: PaginationFilter,
        **kwargs,
    ) -> Page[BaseModel]:
        """List paginated objects"""
        user_list = await list_filters.filter(
            self.model.filter(deleted=False, **kwargs)
        )
        user_list = await self.serializer_list(user_list.all())
        return page_filter.paginate(user_list)

    async def list(self, **filters) -> List[dict]:
        """List objects"""
        list_objs = await self.controller.list(**filters)
        return await self.serializer_list(objs=list_objs)

    async def add(self, record: dict, authenticated_user: UserModel) -> dict:
        """Add an object"""
        obj_created: BaseModel = await self.controller.add(
            record=record, authenticated_user=authenticated_user
        )
        return self.serializer_obj(obj=obj_created, serializer=self.serializer)

    async def update(
        self, record: dict, pk: int, authenticated_user: UserModel
    ) -> BaseModel:
        """Update an object"""
        obj_updated = await self.controller.update(
            record=record, pk=pk, authenticated_user=authenticated_user
        )
        if not obj_updated:
            raise HTTPException(
                detail={"field": "id", "message": NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return self.serializer_obj(obj_updated, self.serializer)

    async def delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Delete an object"""
        obj: BaseModel = await self.controller.get_obj_or_none(pk=pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await self.controller.delete(pk=obj.id, authenticated_user=authenticated_user)

    async def soft_delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Soft delete an object"""
        await self.update(
            record={"deleted": True}, pk=pk, authenticated_user=authenticated_user
        )

    async def get_by_field(self, field: str, value: str) -> dict:
        """Get an object by a field"""
        obj = await self.controller.get_by_field(field=field, value=value)
        if not obj:
            raise HTTPException(
                detail={"field": field, "message": NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return await self.serializer_obj(obj=obj, serializer=self.serializer)
