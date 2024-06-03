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


class SchedulerStatus(str, Enum):
    """
    Scheduler Status Enum

    WAITING_CONFIRMATION - Waiting confirmation
    CONFIRMED - Confirmed
    CANCELED - Canceled
    DONE - Done
    """

    WAITING_CONFIRMATION = "WAITING_CONFIRMATION"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    DONE = "DONE"
