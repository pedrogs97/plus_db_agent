"""Models for the core application."""

from datetime import datetime

from tortoise import fields
from tortoise.models import Model

from plus_db_agent.config import DEFAULT_DATE_TIME_FORMAT
from plus_db_agent.enums import ActionEnum, GenderEnum, SchedulerStatus, ThemeEnum


class BaseModel(Model):
    """Base model for all models in the application."""

    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True


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
        "core.ProfileModel",
        related_name="users",
        on_delete=fields.SET_NULL,
        null=True,
    )
    clinic: fields.ForeignKeyRelation["ClinicModel"] = fields.ForeignKeyField(
        "core.ClinicModel",
        related_name="users",
        on_delete=fields.SET_NULL,
        null=True,
    )
    licenses: fields.ReverseRelation["LicenseUserModel"]

    def __str__(self):
        return self.full_name

    class Meta:
        table = "users"


class ProfileModel(BaseModel):
    """Model to represent a profile."""

    name = fields.CharField(max_length=255)
    clinic: fields.ForeignKeyRelation["ClinicModel"] = fields.ForeignKeyField(
        "core.ClinicModel",
        related_name="profiles",
        on_delete=fields.NO_ACTION,
        null=True,
    )
    permissions: fields.ManyToManyRelation["PermissionModel"] = fields.ManyToManyField(
        "core.PermissionModel", related_name="profiles"
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
        "core.ClinicModel",
        related_name="subsidiaries",
        on_delete=fields.NO_ACTION,
        null=True,
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
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "core.UserModel", related_name="tokens", on_delete=fields.CASCADE
    )
    refresh_token = fields.CharField(max_length=500)
    expires_at = fields.DatetimeField()
    refresh_expires_at = fields.DatetimeField()

    def __str__(self):
        return self.id

    class Meta:
        table = "tokens"


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

    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "core.UserModel",
        related_name="licenses",
        on_delete=fields.NO_ACTION,
    )
    license: fields.ForeignKeyRelation[LicenseModel] = fields.ForeignKeyField(
        "core.LicenseModel",
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

    license: fields.ForeignKeyRelation[LicenseUserModel] = fields.ForeignKeyField(
        "core.LicenseUserModel",
        related_name="payments",
        on_delete=fields.NO_ACTION,
    )
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_date = fields.DateField()

    def __str__(self):
        return f"{self.license} - {self.value}"

    class Meta:
        table = "payments"


class PatientModel(BaseModel):
    """Model to represent a patient."""

    full_name = fields.CharField(max_length=255)
    taxpayer_id = fields.CharField(max_length=12, null=True)
    birth_date = fields.DateField(null=True)
    gender = fields.CharEnumField(
        enum_type=GenderEnum, max_length=1, default=GenderEnum.O
    )
    phone = fields.CharField(max_length=20, null=True)
    treatments: fields.ReverseRelation["TreatmentPatientModel"]
    urgencies: fields.ReverseRelation["UrgencyModel"]

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        """Calculate the age of the patient."""
        return (datetime.date.today() - self.birth_date).days // 365

    class Meta:
        table = "patients"


class DeskModel(BaseModel):
    """Model to represent a desk."""

    number = fields.CharField(max_length=255)
    vacancy = fields.BooleanField(default=True)
    capacity = fields.IntField(default=1)
    observation = fields.TextField(null=True)

    def __str__(self):
        return self.number

    class Meta:
        table = "desks"


class DocumentModel(BaseModel):
    """Model to represent a document."""

    patient: fields.ForeignKeyRelation[PatientModel] = fields.ForeignKeyField(
        "core.PatientModel",
        related_name="documents",
        on_delete=fields.NO_ACTION,
    )
    file_name = fields.CharField(max_length=255)
    file_path = fields.CharField(max_length=255)
    observation = fields.TextField(null=True)

    def __str__(self):
        return f"{self.patient} - {self.file_name}"

    class Meta:
        table = "documents"


class TreatmentModel(BaseModel):
    """Model to represent a treatment."""

    name = fields.CharField(max_length=255)
    number = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    cost = fields.DecimalField(max_digits=10, decimal_places=2)
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    observation = fields.TextField(null=True)

    def __str__(self):
        return f"{self.name} - {self.number}"

    class Meta:
        table = "treatments"


class TreatmentPatientModel(BaseModel):
    """Model to represent the relationship between a treatment and a patient."""

    patient: fields.ForeignKeyRelation[PatientModel] = fields.ForeignKeyField(
        "core.PatientModel",
        related_name="treatments",
        on_delete=fields.NO_ACTION,
    )
    treatment: fields.ForeignKeyRelation[TreatmentModel] = fields.ForeignKeyField(
        "core.TreatmentModel",
        related_name="patients",
        on_delete=fields.NO_ACTION,
    )
    start_date = fields.DateField()
    end_date = fields.DateField(null=True)
    observation = fields.TextField(null=True)

    def __str__(self):
        return f"{self.patient} - {self.treatment}"

    class Meta:
        table = "treatments_patients"


class UrgencyModel(BaseModel):
    """Model to represent an urgency."""

    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    observation = fields.TextField(null=True)
    patient: fields.ForeignKeyRelation[PatientModel] = fields.ForeignKeyField(
        "core.PatientModel",
        related_name="urgencies",
        on_delete=fields.NO_ACTION,
    )
    date = fields.DateField()

    def __str__(self):
        return self.name

    class Meta:
        table = "urgencies"


class AnamnesisModel(BaseModel):
    """Model to represent an anamnesis."""

    name = fields.CharField(max_length=255)
    number = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    observation = fields.TextField(null=True)
    questions: fields.ReverseRelation["QuestionModel"]

    def __str__(self):
        return f"{self.name} - {self.number}"

    class Meta:
        table = "anamnesis"


class QuestionModel(BaseModel):
    """Model to represent a question."""

    anamnesis: fields.ForeignKeyRelation[AnamnesisModel] = fields.ForeignKeyField(
        "core.AnamnesisModel",
        related_name="questions",
        on_delete=fields.NO_ACTION,
    )
    question = fields.TextField()
    short_question = fields.BooleanField(default=False)

    def __str__(self):
        return f"{self.anamnesis} - {self.question}"

    class Meta:
        table = "questions"


class AnswerModel(BaseModel):
    """Model to represent an answer."""

    question: fields.ForeignKeyRelation[QuestionModel] = fields.ForeignKeyField(
        "core.QuestionModel",
        related_name="answers",
        on_delete=fields.NO_ACTION,
    )
    patient: fields.ForeignKeyRelation[PatientModel] = fields.ForeignKeyField(
        "core.PatientModel",
        related_name="answers",
        on_delete=fields.NO_ACTION,
    )
    answer = fields.TextField()

    def __str__(self):
        return f"{self.question} - {self.answer}"

    class Meta:
        table = "answers"


class PlanModel(BaseModel):
    """Model to represent a plan."""

    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    observation = fields.TextField(null=True)
    specialties: fields.ManyToManyRelation["SpecialtyModel"] = fields.ManyToManyField(
        "core.SpecialtyModel", related_name="plans"
    )

    def __str__(self):
        return self.name

    class Meta:
        table = "plans"


class SpecialtyModel(BaseModel):
    """Model to represent a specialty."""

    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "specialties"


class PlanTreatmentModel(BaseModel):
    """Model to represent the relationship between a plan and a treatment."""

    plan: fields.ForeignKeyRelation[PlanModel] = fields.ForeignKeyField(
        "core.PlanModel",
        related_name="treatments",
        on_delete=fields.NO_ACTION,
    )
    treatment: fields.ForeignKeyRelation[TreatmentModel] = fields.ForeignKeyField(
        "core.TreatmentModel",
        related_name="plans",
        on_delete=fields.NO_ACTION,
    )
    observation = fields.TextField(null=True)

    def __str__(self):
        return f"{self.plan} - {self.treatment}"

    class Meta:
        table = "plans_treatments"


class LogModel(BaseModel):
    """Log model"""

    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "core.UserModel", related_name="logs", on_delete=fields.SET_NULL, null=True
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


class SchedulerModel(BaseModel):
    """Model to represent a scheduler."""

    status = fields.CharEnumField(
        enum_type=SchedulerStatus,
        max_length=20,
        default=SchedulerStatus.WAITING_CONFIRMATION,
    )
    date = fields.DatetimeField()
    description = fields.TextField(null=True)
    is_return = fields.BooleanField(default=False)
    is_off = fields.BooleanField(default=False)
    off_reason = fields.TextField(null=True)
    clinic_id = fields.BigIntField()
    patient = fields.CharField(max_length=150)
    user = fields.CharField(max_length=150)
    desk = fields.CharField(max_length=150)

    def __str__(self):
        return f"{self.date} - {self.status}"

    class Meta:
        table = "schedulers"


class HolidayModel(BaseModel):
    """Model to represent a holiday."""

    date = fields.DatetimeField()
    name = fields.CharField(max_length=100)
    type = fields.CharField(max_length=100)
    level = fields.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.name}"

    class Meta:
        table = "holidays"
