from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clinics" ADD "head_quarter_id" BIGINT;
        ALTER TABLE "clinics" ADD CONSTRAINT "fk_clinics_clinics_00560b85" FOREIGN KEY ("head_quarter_id") REFERENCES "clinics" ("id") ON DELETE NO ACTION;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clinics" DROP CONSTRAINT "fk_clinics_clinics_00560b85";
        ALTER TABLE "clinics" DROP COLUMN "head_quarter_id";"""
