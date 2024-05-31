"""Project Enums"""

from enum import Enum


class GenderEnum(str, Enum):
    """
    Gender Enum

    M - Male
    F - Female
    O - Other
    """

    M = "M"
    F = "F"
    O = "O"


class ActionEnum(str, Enum):
    """
    Action Enum

    CREATE - Create
    UPDATE - Update
    DELETE - Delete
    VIEW   - View
    """

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VIEW = "VIEW"


class ThemeEnum(str, Enum):
    """
    Theme Enum

    LIGHT - Light
    DARK  - Dark
    """

    LIGHT = "LIGHT"
    DARK = "DARK"
