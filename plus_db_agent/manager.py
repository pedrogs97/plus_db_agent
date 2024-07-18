"""Manager for the database"""

import os

from tortoise import Tortoise, connections
from tortoise.exceptions import OperationalError

from plus_db_agent.config import DATABASE_CONFIG, DEBUG, bcrypt_context
from plus_db_agent.logger import logger
from plus_db_agent.models import ClinicModel, ProfileModel, UserModel


def hash_password(password: str) -> str:
    """Hash password"""
    return bcrypt_context.hash(password)


async def __create_superuser():
    """Create a test user"""
    clinic, _ = await ClinicModel.get_or_create(
        defaults={
            "company_name": "Clinic Test",
            "company_register_number": "97.169.561/0001-50",
            "address": "Rua Teste, 123",
            "subdomain": "teste",
        }
    )
    logger.debug(clinic)
    profile_manager, _ = await ProfileModel.get_or_create(
        defaults={"name": "Manager"}
        # defaults={"name": "Manager", "clinic": clinic}
    )
    await UserModel.get_or_create(
        defaults={
            "full_name": os.getenv("DEFAULT_SUPERUSER_FULL_NAME", "Test User"),
            "password": hash_password(
                os.getenv("DEFAULT_SUPERUSER_PASSWORD", "123456")
            ),
            "email": os.getenv("DEFAULT_SUPERUSER_EMAIL", "teste@email.com"),
            "username": os.getenv("DEFAULT_SUPERUSER_USERNAME", "test"),
            "is_superuser": True,
            "profile_id": profile_manager.id,
            # "clinic_id": clinic.id,
        }
    )


async def close():
    """Close all connections"""
    logger.info("Closing database connections")
    await connections.close_all()
    await Tortoise.close_connections()


async def init():
    """Init the database"""
    logger.info("Initializing database")
    await Tortoise.init(config=DATABASE_CONFIG)
    # await Tortoise.generate_schemas()
    try:
        if DEBUG:
            logger.info("Trying create superuser")
            await __create_superuser()
    except OperationalError as err:
        if DEBUG:
            logger.info("Error creating superuser: %s", err)
