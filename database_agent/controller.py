"""Base service class that will be inherited by all other services"""
import logging
from typing import Union

from tortoise.exceptions import IntegrityError

from database_agent.models import LogModel, T, UserModel
from database_agent.repository import GenericRepository

logger = logging.getLogger(__name__)


class GenericController:
    """Base service class that will be inherited by all other services"""

    model: T
    repository = GenericRepository()
    module_name = "base"

    def __set_log(
        self,
        module: str,
        model: str,
        operation: str,
        identifier: int,
        user: UserModel,
    ) -> bool:
        """Set a log from a operation"""
        try:
            new_log = LogModel(
                user=user,
                module=module,
                model=model,
                operation=operation,
                identifier=identifier,
            )
            new_log.save()
            return True
        except IntegrityError as error:
            logger.error("Error setting log: %s", error)
            return False

    async def get_obj_or_none(self, pk: int) -> Union[T, None]:
        """Get an object by its id or raise a none error"""
        return await self.repository.get_by_id(pk)

    async def list(self, **filters) -> list[T]:
        """List objects"""
        return await self.repository.list(**filters)

    async def add(self, record: dict, authenticated_user: UserModel) -> T:
        """Add an object"""
        obj_created: T = await self.repository.add(record)
        self.__set_log(
            module=self.module_name,
            model=self.model.__name__,
            operation="Criação",
            identifier=obj_created.id,
            user=authenticated_user,
        )
        return obj_created

    async def update(
        self, record: dict, pk: int, authenticated_user: UserModel
    ) -> Union[T, None]:
        """Update an object"""
        obj = await self.get_obj_or_none(pk)
        if not obj:
            return None
        obj_updated: T = await self.repository.update(obj, record)
        self.__set_log(
            module=self.module_name,
            model=self.model.__name__,
            operation="Atualização",
            identifier=obj_updated.id,
            user=authenticated_user,
        )
        return obj_updated

    async def delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Delete an object"""
        obj: T = await self.get_obj_or_none(pk)
        await self.repository.delete(obj.id)
        self.__set_log(
            module=self.module_name,
            model=self.model.__name__,
            operation="Exclusão permanente",
            identifier=None,
            user=authenticated_user,
        )

    async def soft_delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Soft delete an object"""
        obj_updated: T = self.update({"deleted": True}, pk, authenticated_user)
        self.__set_log(
            module=self.module_name,
            model=self.model.__name__,
            operation="Exclusão",
            identifier=obj_updated.id,
            user=authenticated_user,
        )

    async def get_by_field(self, field: str, value: str) -> Union[T, None]:
        """Get an object by a field"""
        return await self.repository.get_by_field(field, value)
