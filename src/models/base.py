"""Provides the base model for all models in the application."""

from typing import TypeVar

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """Base model for all models in the application."""

    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True


T = TypeVar("T", bound=BaseModel)
