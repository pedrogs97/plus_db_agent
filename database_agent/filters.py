"""Base filter for Tortoise orm related filters."""
from typing import Union

from fastapi_filter.base.filter import BaseFilterModel
from pydantic import ValidationInfo, field_validator
from tortoise.expressions import Q
from tortoise.queryset import QuerySet, QuerySetSingle


class Filter(BaseFilterModel):
    """Base filter for Tortoise orm related filters."""

    @field_validator("*", mode="before")
    def split_str(
        cls, value, field: ValidationInfo
    ):  # pylint: disable=no-self-argument
        """Split string values."""
        if (
            field.field_name is not None
            and (
                field.field_name == cls.Constants.ordering_field_name
                or field.field_name.endswith("__in")
                or field.field_name.endswith("__not_in")
            )
            and isinstance(value, str)
        ):
            if not value:
                # Empty string should return [] not ['']
                return []
            return list(value.split(","))
        return value

    def filter(self, query: Union[QuerySet, QuerySetSingle]):
        for field_name, value in self.filtering_fields:
            if field_name == self.Constants.search_field_name and hasattr(
                self.Constants, "search_model_fields"
            ):
                search_filters = map(
                    lambda field, value=value: Q(**{field: value}),
                    self.Constants.search_model_fields,
                )
                query = query.filter(*search_filters)
            else:
                query = query.filter(**{field_name: value})

        return query

    def sort(self, query: Union[QuerySet, QuerySetSingle]):
        if not self.ordering_values:
            return query

        query = query.order_by(*self.ordering_values)

        return query
