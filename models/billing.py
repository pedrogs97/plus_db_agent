"""Models for the billing app."""

from tortoise import fields

from models import BaseModel


class LicenseModel(BaseModel):
    """Model to represent a license."""

    license_number = fields.CharField(max_length=20)
    modules = fields.CharField(max_length=255)
    value = fields.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.license_number}"

    class Meta:
        table = "licenses"


class LicenseUserModel(BaseModel):
    """Model to represent the relationship between a license and a user."""

    user = fields.ForeignKeyField(
        "models.UserModel",
        related_name="licenses",
        on_delete=fields.NO_ACTION,
    )
    license = fields.ForeignKeyField(
        "models.LicenseModel",
        related_name="users",
        on_delete=fields.NO_ACTION,
    )
    start_date = fields.DateField()
    end_date = fields.DateField()
    observation = fields.TextField(null=True)
    off_percentage = fields.DecimalField(max_digits=10, decimal_places=2)
    credit = fields.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.license}"

    class Meta:
        table = "licenses_users"


class PaymentModel(BaseModel):
    """Model to represent a payment."""

    license = fields.ForeignKeyField(
        "models.LicenseUserModel",
        related_name="payments",
        on_delete=fields.NO_ACTION,
    )
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_date = fields.DateField()

    def __str__(self):
        return f"{self.license} - {self.value}"

    class Meta:
        table = "payments"
