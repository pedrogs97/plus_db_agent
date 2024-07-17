from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "anamnesis" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "number" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "observation" TEXT
);
COMMENT ON TABLE "anamnesis" IS 'Model to represent an anamnesis.';
CREATE TABLE IF NOT EXISTS "clinics" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "company_name" VARCHAR(255) NOT NULL,
    "company_register_number" VARCHAR(20) NOT NULL,
    "legal_entity" BOOL NOT NULL  DEFAULT False,
    "address" VARCHAR(255) NOT NULL,
    "subdomain" VARCHAR(255) NOT NULL UNIQUE,
    "logo_path" VARCHAR(255),
    "head_quarter_id" BIGINT REFERENCES "clinics" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "clinics" IS 'Model to represent a clinic.';
CREATE TABLE IF NOT EXISTS "desks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "number" VARCHAR(255) NOT NULL,
    "vacancy" BOOL NOT NULL  DEFAULT True,
    "capacity" INT NOT NULL  DEFAULT 1,
    "observation" TEXT
);
COMMENT ON TABLE "desks" IS 'Model to represent a desk.';
CREATE TABLE IF NOT EXISTS "holidays" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "date" TIMESTAMPTZ NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "type" VARCHAR(100) NOT NULL,
    "level" VARCHAR(100) NOT NULL
);
COMMENT ON TABLE "holidays" IS 'Model to represent a holiday.';
CREATE TABLE IF NOT EXISTS "licenses" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "license_number" VARCHAR(20) NOT NULL,
    "modules" VARCHAR(255) NOT NULL,
    "value" DECIMAL(10,2) NOT NULL
);
COMMENT ON TABLE "licenses" IS 'Model to represent a license.';
CREATE TABLE IF NOT EXISTS "patients" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "full_name" VARCHAR(255) NOT NULL,
    "taxpayer_id" VARCHAR(12),
    "birth_date" DATE,
    "gender" VARCHAR(1) NOT NULL  DEFAULT 'O',
    "phone" VARCHAR(20)
);
COMMENT ON COLUMN "patients"."gender" IS 'M: M\nF: F\nO: O';
COMMENT ON TABLE "patients" IS 'Model to represent a patient.';
CREATE TABLE IF NOT EXISTS "documents" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "file_name" VARCHAR(255) NOT NULL,
    "file_path" VARCHAR(255) NOT NULL,
    "observation" TEXT,
    "patient_id" BIGINT NOT NULL REFERENCES "patients" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "documents" IS 'Model to represent a document.';
CREATE TABLE IF NOT EXISTS "permissions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "module" VARCHAR(255) NOT NULL,
    "model" VARCHAR(255) NOT NULL,
    "action" VARCHAR(6) NOT NULL  DEFAULT 'VIEW',
    "description" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "permissions"."action" IS 'CREATE: CREATE\nUPDATE: UPDATE\nDELETE: DELETE\nVIEW: VIEW';
COMMENT ON TABLE "permissions" IS 'Model to represent a permission.';
CREATE TABLE IF NOT EXISTS "plans" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "observation" TEXT
);
COMMENT ON TABLE "plans" IS 'Model to represent a plan.';
CREATE TABLE IF NOT EXISTS "profiles" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "clinic_id" BIGINT REFERENCES "clinics" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "profiles" IS 'Model to represent a profile.';
CREATE TABLE IF NOT EXISTS "prospections_stages" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "color" VARCHAR(7) NOT NULL
);
COMMENT ON TABLE "prospections_stages" IS 'Model to represent a prospection stage.';
CREATE TABLE IF NOT EXISTS "prospections" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "full_name" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(20) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "observation" TEXT,
    "gender" VARCHAR(1) NOT NULL  DEFAULT 'O',
    "birth_date" DATE,
    "clinic_id" BIGINT NOT NULL REFERENCES "clinics" ("id") ON DELETE NO ACTION,
    "stage_id" BIGINT NOT NULL REFERENCES "prospections_stages" ("id") ON DELETE NO ACTION
);
COMMENT ON COLUMN "prospections"."gender" IS 'M: M\nF: F\nO: O';
COMMENT ON TABLE "prospections" IS 'Model to represent a prospection.';
CREATE TABLE IF NOT EXISTS "questions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "question" TEXT NOT NULL,
    "short_question" BOOL NOT NULL  DEFAULT False,
    "anamnesis_id" BIGINT NOT NULL REFERENCES "anamnesis" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "questions" IS 'Model to represent a question.';
CREATE TABLE IF NOT EXISTS "answers" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "answer" TEXT NOT NULL,
    "patient_id" BIGINT NOT NULL REFERENCES "patients" ("id") ON DELETE NO ACTION,
    "question_id" BIGINT NOT NULL REFERENCES "questions" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "answers" IS 'Model to represent an answer.';
CREATE TABLE IF NOT EXISTS "schedulers" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'WAITING_CONFIRMATION',
    "date" TIMESTAMPTZ NOT NULL,
    "description" TEXT,
    "is_return" BOOL NOT NULL  DEFAULT False,
    "is_off" BOOL NOT NULL  DEFAULT False,
    "off_reason" TEXT,
    "clinic_id" BIGINT NOT NULL,
    "patient" VARCHAR(150) NOT NULL,
    "user" VARCHAR(150) NOT NULL,
    "desk" VARCHAR(150) NOT NULL
);
COMMENT ON COLUMN "schedulers"."status" IS 'WAITING_CONFIRMATION: WAITING_CONFIRMATION\nCONFIRMED: CONFIRMED\nCANCELED: CANCELED\nDONE: DONE\nWAITING: WAITING';
COMMENT ON TABLE "schedulers" IS 'Model to represent a scheduler.';
CREATE TABLE IF NOT EXISTS "specialties" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT
);
COMMENT ON TABLE "specialties" IS 'Model to represent a specialty.';
CREATE TABLE IF NOT EXISTS "treatments" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "number" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "cost" DECIMAL(10,2) NOT NULL,
    "value" DECIMAL(10,2) NOT NULL,
    "observation" TEXT
);
COMMENT ON TABLE "treatments" IS 'Model to represent a treatment.';
CREATE TABLE IF NOT EXISTS "plans_treatments" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "observation" TEXT,
    "plan_id" BIGINT NOT NULL REFERENCES "plans" ("id") ON DELETE NO ACTION,
    "treatment_id" BIGINT NOT NULL REFERENCES "treatments" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "plans_treatments" IS 'Model to represent the relationship between a plan and a treatment.';
CREATE TABLE IF NOT EXISTS "treatments_patients" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "start_date" DATE NOT NULL,
    "end_date" DATE,
    "observation" TEXT,
    "patient_id" BIGINT NOT NULL REFERENCES "patients" ("id") ON DELETE NO ACTION,
    "treatment_id" BIGINT NOT NULL REFERENCES "treatments" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "treatments_patients" IS 'Model to represent the relationship between a treatment and a patient.';
CREATE TABLE IF NOT EXISTS "urgencies" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "observation" TEXT,
    "date" DATE NOT NULL,
    "patient_id" BIGINT NOT NULL REFERENCES "patients" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "urgencies" IS 'Model to represent an urgency.';
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "full_name" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "taxpayer_id" VARCHAR(12),
    "phone" VARCHAR(20),
    "profile_picture_path" VARCHAR(255),
    "is_clinic_master" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "theme" VARCHAR(5) NOT NULL  DEFAULT 'LIGHT',
    "last_login_in" TIMESTAMPTZ,
    "clinic_id" BIGINT REFERENCES "clinics" ("id") ON DELETE SET NULL,
    "profile_id" BIGINT REFERENCES "profiles" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "users"."theme" IS 'LIGHT: LIGHT\nDARK: DARK';
COMMENT ON TABLE "users" IS 'Model to represent a user.';
CREATE TABLE IF NOT EXISTS "licenses_users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "observation" TEXT,
    "off_percentage" DECIMAL(10,2) NOT NULL,
    "credit" DECIMAL(10,2) NOT NULL,
    "license_id" BIGINT NOT NULL REFERENCES "licenses" ("id") ON DELETE NO ACTION,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "licenses_users" IS 'Model to represent the relationship between a license and a user.';
CREATE TABLE IF NOT EXISTS "logs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "module" VARCHAR(100) NOT NULL,
    "model" VARCHAR(100) NOT NULL,
    "operation" VARCHAR(150) NOT NULL,
    "identifier" INT,
    "logged_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "logs" IS 'Log model';
CREATE TABLE IF NOT EXISTS "payments" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "value" DECIMAL(10,2) NOT NULL,
    "payment_date" DATE NOT NULL,
    "license_id" BIGINT NOT NULL REFERENCES "licenses_users" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "payments" IS 'Model to represent a payment.';
CREATE TABLE IF NOT EXISTS "tokens" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "token" VARCHAR(500) NOT NULL,
    "refresh_token" VARCHAR(500) NOT NULL,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "refresh_expires_at" TIMESTAMPTZ NOT NULL,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tokens" IS 'Model to represent a token.';
CREATE TABLE IF NOT EXISTS "plans_specialties" (
    "plans_id" BIGINT NOT NULL REFERENCES "plans" ("id") ON DELETE CASCADE,
    "specialtymodel_id" BIGINT NOT NULL REFERENCES "specialties" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_plans_speci_plans_i_990a06" ON "plans_specialties" ("plans_id", "specialtymodel_id");
CREATE TABLE IF NOT EXISTS "profiles_permissions" (
    "profiles_id" BIGINT NOT NULL REFERENCES "profiles" ("id") ON DELETE CASCADE,
    "permissionmodel_id" BIGINT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_profiles_pe_profile_f099a6" ON "profiles_permissions" ("profiles_id", "permissionmodel_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
