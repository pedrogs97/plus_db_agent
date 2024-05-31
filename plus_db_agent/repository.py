"""This module contains the generic repository class"""

from typing import List, Optional, Type

from plus_db_agent.models import BaseModel


class GenericRepository:
    """Generic repository class that will be inherited by all other repositories"""

    model: Type[BaseModel]

    async def get_by_id(self, pk: int) -> Optional[BaseModel]:
        """Get a record by its pk"""
        return await self.model.get_or_none(id=pk)

    async def list(self, **filters) -> List[BaseModel]:
        """List records"""
        if "ordering" in filters:
            ordering = filters.pop("ordering")
            return await self.model.filter(**filters).order_by(*ordering)
        return await self.model.filter(**filters).order_by("-created_at")

    async def add(self, record: dict) -> BaseModel:
        """Add a record"""
        return await self.model.create(**record)

    async def update(self, record: dict, instance: BaseModel) -> BaseModel:
        """Update a record"""
        for key, value in record.items():
            if hasattr(instance, key) and key != "id" and value is not None:
                setattr(instance, key, value)
        await instance.save()

    async def delete(self, pk: int) -> None:
        """Delete a record by its pk"""
        instance: BaseModel = await self.get_by_id(pk=pk)
        await instance.delete()

    async def get_by_field(self, field: str, value: str) -> Optional[BaseModel]:
        """Get a record by a field"""
        return await self.model.get_or_none(**{field: value})
