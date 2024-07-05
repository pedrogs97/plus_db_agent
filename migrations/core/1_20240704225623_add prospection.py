from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
CREATE TABLE IF NOT EXISTS "prospections_stages" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(255) NOT NULL,
    "color" VARCHAR(7) NOT NULL
);
CREATE TABLE IF NOT EXISTS "prospections" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL  DEFAULT False,
    "full_name" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(20) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "observation" TEXT,
    "clinic_id" BIGINT NOT NULL REFERENCES "clinics" ("id") ON DELETE NO ACTION,
    "stage_id" BIGINT NOT NULL REFERENCES "prospections_stages" ("id") ON DELETE NO ACTION
);
COMMENT ON TABLE "prospections" IS 'Model to represent a prospection.';
COMMENT ON TABLE "prospections_stages" IS 'Model to represent a prospection stage.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "prospections";
        DROP TABLE IF EXISTS "prospections_stages";"""
