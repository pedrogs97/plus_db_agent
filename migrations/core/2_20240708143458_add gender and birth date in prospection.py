from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "prospections" ADD "birth_date" DATE;
        ALTER TABLE "prospections" ADD "gender" VARCHAR(1) NOT NULL  DEFAULT 'O';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "prospections" DROP COLUMN "birth_date";
        ALTER TABLE "prospections" DROP COLUMN "gender";"""
