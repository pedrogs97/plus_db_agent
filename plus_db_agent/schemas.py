"""Base schemas for all schemas in the application"""

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from plus_db_agent.enums import BaseMessageType


class BaseSchema(BaseModel):
    """Base schema"""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")


class ConnectionSchema(BaseSchema):
    """Connection Schema"""

    token: str


class CreateUUIDSchema(BaseSchema):
    """Create UUID Schema"""

    uuid: str


class ErrorResponseSchema(BaseSchema):
    """Error Response Schema"""

    error: str


class Message(BaseSchema):
    """Message Schema"""

    message_type: BaseMessageType = Field(alias="messageType")
    clinic_id: int = Field(alias="clinicId")
    data: Optional[
        Union[
            ConnectionSchema,
            CreateUUIDSchema,
            ErrorResponseSchema,
        ]
    ] = None
