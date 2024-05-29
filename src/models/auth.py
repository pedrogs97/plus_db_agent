"""Models for the auth app."""

from tortoise import fields

from src.enums import ActionEnum, ThemeEnum
from src.models import BaseModel


class UserModel(BaseModel):
    """Model to represent a user."""

    full_name = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    taxpayer_id = fields.CharField(max_length=12, null=True)
    phone = fields.CharField(max_length=20, null=True)
    profile_picture_path = fields.CharField(max_length=255, null=True)
    is_clinic_master = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    theme = fields.CharEnumField(
        enum_type=ThemeEnum, max_length=5, default=ThemeEnum.LIGHT
    )
    last_login_in = fields.DatetimeField(null=True)
    profile: fields.ForeignKeyRelation["ProfileModel"] = fields.ForeignKeyField(
        "models.ProfileModel",
        related_name="users",
        on_delete=fields.SET_NULL,
        null=True,
    )
    clinic: fields.ForeignKeyRelation["ClinicModel"] = fields.ForeignKeyField(
        "models.ClinicModel",
        related_name="users",
        on_delete=fields.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.full_name

    class Meta:
        table = "users"


class ProfileModel(BaseModel):
    """Model to represent a profile."""

    name = fields.CharField(max_length=255)
    clinic = fields.ForeignKeyField(
        "models.ClinicModel",
        related_name="profiles",
        on_delete=fields.NO_ACTION,
        null=True,
    )
    permissions = fields.ManyToManyField(
        "models.PermissionModel", related_name="profiles"
    )

    def __str__(self):
        return self.name

    class Meta:
        table = "profiles"


class PermissionModel(BaseModel):
    """Model to represent a permission."""

    module = fields.CharField(max_length=255)
    model = fields.CharField(max_length=255)
    action = fields.CharEnumField(
        enum_type=ActionEnum, max_length=6, default=ActionEnum.VIEW
    )
    description = fields.CharField(max_length=255)

    def __str__(self):
        return f"{self.module} - {self.model} - {self.action}"

    class Meta:
        table = "permissions"


class ClinicModel(BaseModel):
    """Model to represent a clinic."""

    head_quarter: fields.ForeignKeyRelation["ClinicModel"] = fields.ForeignKeyField(
        "models.ClinicModel",
        related_name="subsidiaries",
        on_delete=fields.NO_ACTION,
        null=True,
    )
    license: fields.ForeignKeyRelation["LicenseModel"] = fields.ForeignKeyField(
        "models.LicenseModel",
        related_name="clinics",
        on_delete=fields.NO_ACTION,
    )
    company_name = fields.CharField(max_length=255)
    company_register_number = fields.CharField(max_length=20)
    legal_entity = fields.BooleanField(default=False)
    address = fields.CharField(max_length=255)
    subdomain = fields.CharField(max_length=255, unique=True)
    logo_path = fields.CharField(max_length=255, null=True)

    users: fields.ReverseRelation["UserModel"]

    def __str__(self):
        return f"{self.company_name} - {self.legal_entity}"

    class Meta:
        table = "clinics"


class TokenModel(BaseModel):
    """Model to represent a token."""

    token = fields.CharField(max_length=500)
    user = fields.ForeignKeyField(
        "models.UserModel", related_name="tokens", on_delete=fields.CASCADE
    )
    refresh_token = fields.CharField(max_length=500)
    expires_at = fields.DatetimeField()
    refresh_expires_at = fields.DatetimeField()

    def __str__(self):
        return self.id

    class Meta:
        table = "tokens"
