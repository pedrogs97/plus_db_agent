"""Base filter for Tortoise orm related filters."""

from collections import defaultdict
from typing import Annotated, Optional, Union, get_type_hints

from fastapi import Query
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ValidationInfo, field_validator
from tortoise.expressions import Q
from tortoise.queryset import QuerySet, QuerySetSingle

from plus_db_agent.models import BaseModel, T


class BaseFilter(PydanticBaseModel):
    """Base filter for Tortoise orm related filters."""

    class Constants:
        """Constants for the base filter."""

        model: T
        ordering_field_name: str = "order_by"
        search_model_fields: list[str]
        search_field_name: str = "search"
        prefix: str
        original_filter: type["BaseFilter"]

    @property
    def filtering_fields(self):
        """Get filtering fields."""
        fields = self.model_dump(exclude_none=True, exclude_unset=True)
        fields.pop(self.Constants.ordering_field_name, None)
        return fields.items()

    @property
    def ordering_values(self):
        """Check that the ordering field is present on the class definition."""
        try:
            return getattr(self, self.Constants.ordering_field_name)
        except AttributeError as e:
            raise AttributeError(
                f"Ordering field {self.Constants.ordering_field_name} is not defined. "
                "Make sure to add it to your filter class."
            ) from e

    @field_validator("*", mode="before", check_fields=False)
    def strip_order_by_values(
        cls, value: Optional[str], field: ValidationInfo
    ):  # pylint: disable=no-self-argument
        """Strip ordering values."""
        if field.field_name != cls.Constants.ordering_field_name:
            return value

        if not value:
            return None

        stripped_values = []
        for field_name in value:
            stripped_value = field_name.strip()
            if stripped_value:
                stripped_values.append(stripped_value)

        return stripped_values

    @field_validator("*", mode="before", check_fields=False)
    def validate_order_by(
        cls, value: Optional[str], field: ValidationInfo
    ):  # pylint: disable=no-self-argument
        """Validate ordering values."""
        if field.field_name != cls.Constants.ordering_field_name:
            return value

        if not value:
            return None

        field_name_usages = defaultdict(list)
        duplicated_field_names = set()

        for field_name_with_direction in value:
            field_name = field_name_with_direction.replace("-", "").replace("+", "")

            if not hasattr(cls.Constants.model, field_name):
                raise ValueError(f"{field_name} is not a valid ordering field.")

            field_name_usages[field_name].append(field_name_with_direction)
            if len(field_name_usages[field_name]) > 1:
                duplicated_field_names.add(field_name)

        if duplicated_field_names:
            ambiguous_field_names = ", ".join(
                [
                    field_name_with_direction
                    for field_name in sorted(duplicated_field_names)
                    for field_name_with_direction in field_name_usages[field_name]
                ]
            )
            raise ValueError(
                f"Field names can appear at most once for {cls.Constants.ordering_field_name}. "
                f"The following was ambiguous: {ambiguous_field_names}."
            )

        return value

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

    async def filter(self, query: Union[QuerySet, QuerySetSingle]):
        """Filter the query."""
        hints = get_type_hints(self.Constants.model)
        hints_dict = {field: field_type for field, field_type in hints.items()}
        for field_name, value in self.filtering_fields:
            if (
                "__" in field_name
                and field_name in hints_dict
                and issubclass(hints_dict[field_name], BaseModel)
            ):
                related_field_name = field_name.split("__")[0]
                await query.prefetch_related(related_field_name)
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
        """Sort the query."""
        if not self.ordering_values:
            return query

        query = query.order_by(*self.ordering_values)

        return query


class PaginationFilter:
    """Filter for pagination."""

    def __init__(
        self,
        page: Annotated[int, Query(title="Page number")],
        size: Annotated[int, Query(title="Page size")],
    ):
        self.page = page
        self.size = size
