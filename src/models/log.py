"""Log models"""
from tortoise import fields

from src.config import DEFAULT_DATE_TIME_FORMAT
from src.models import BaseModel, UserModel


class LogModel(BaseModel):
    """Log model"""

    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel", related_name="logs", on_delete=fields.SET_NULL, null=True
    )

    module = fields.CharField(max_length=100)
    model = fields.CharField(max_length=100)
    operation = fields.CharField(max_length=150)
    identifier = fields.IntField(null=True)
    logged_in = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        date_str = self.logged_in.strftime(DEFAULT_DATE_TIME_FORMAT)
        return f"{self.module}:{self.operation} - {date_str}"

    class Meta:
        table = "logs"
