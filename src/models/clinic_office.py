"""This module contains the models of the clinic_office app."""

import datetime

from tortoise import fields

from src.enums import GenderEnum
from src.models import BaseModel


class PatientModel(BaseModel):
    """Model to represent a patient."""

    full_name = fields.CharField(max_length=255)
    taxpayer_id = fields.CharField(max_length=12, null=True)
    birth_date = fields.DateField(null=True)
    gender = fields.CharEnumField(
        enum_type=GenderEnum, max_length=1, default=GenderEnum.O
    )
    phone = fields.CharField(max_length=20, null=True)

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

    patient = fields.ForeignKeyField(
        "models.PatientModel",
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

    patient = fields.ForeignKeyField(
        "models.PatientModel",
        related_name="treatments",
        on_delete=fields.NO_ACTION,
    )
    treatment = fields.ForeignKeyField(
        "models.TreatmentModel",
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

    def __str__(self):
        return f"{self.name} - {self.number}"

    class Meta:
        table = "anamnesis"


class QuestionModel(BaseModel):
    """Model to represent a question."""

    anamnesis = fields.ForeignKeyField(
        "models.AnamnesisModel",
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

    question = fields.ForeignKeyField(
        "models.QuestionModel",
        related_name="answers",
        on_delete=fields.NO_ACTION,
    )
    patient = fields.ForeignKeyField(
        "models.PatientModel",
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
    specialities = fields.ManyToManyField("models.SpecialtyModel", related_name="plans")

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

    plan = fields.ForeignKeyField(
        "models.PlanModel",
        related_name="treatments",
        on_delete=fields.NO_ACTION,
    )
    treatment = fields.ForeignKeyField(
        "models.TreatmentModel",
        related_name="plans",
        on_delete=fields.NO_ACTION,
    )
    observation = fields.TextField(null=True)

    def __str__(self):
        return f"{self.plan} - {self.treatment}"

    class Meta:
        table = "plans_treatments"
