"""Base service class that will be inherited by all other services"""

from typing import Union

from fastapi import status
from fastapi.exceptions import HTTPException

from controller import GenericController
from models import T, UserModel


class GenericService:
    """Base service class that will be inherited by all other services"""

    model: T
    controller = GenericController()
    module_name = "base"

    async def get_obj_or_404(self, pk: int) -> T:
        """Get an object by its id or raise a 404 error"""
        obj = await self.controller.get_obj_or_none(pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return obj

    async def list(self, **filters) -> list[T]:
        """List objects"""
        return await self.controller.list(**filters)

    async def add(self, record: dict, authenticated_user: UserModel) -> T:
        """Add an object"""
        obj_created: T = await self.controller.add(record, authenticated_user)
        return obj_created

    async def update(self, record: dict, pk: int, authenticated_user: UserModel) -> T:
        """Update an object"""
        obj_updated = await self.controller.update(record, pk, authenticated_user)
        if not obj_updated:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return obj_updated

    async def delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Delete an object"""
        obj: T = await self.get_obj_or_404(pk)
        if not obj:
            raise HTTPException(
                detail={"field": "id", "message": "Não encontrado"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await self.controller.delete(obj.id, authenticated_user)

    async def soft_delete(self, pk: int, authenticated_user: UserModel) -> None:
        """Soft delete an object"""
        await self.update({"deleted": True}, pk, authenticated_user)

    async def get_by_field(self, field: str, value: str) -> Union[T, None]:
        """Get an object by a field"""
        return await self.controller.get_by_field(field, value)
