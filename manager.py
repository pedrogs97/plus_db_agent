"""Manager for the database"""
import os

from tortoise import Tortoise, connections

from .config import DATABASE_CONFIG, bcrypt_context
from .models import ProfileModel, UserModel


def hash_password(password: str) -> str:
    """Hash password"""
    return bcrypt_context.hash(password)


async def __create_superuser():
    """Create a test user"""
    profile_manager, _ = await ProfileModel.get_or_create(defaults={"name": "Manager"})
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
        }
    )


async def close():
    """Close all connections"""
    await connections.close_all()
    await Tortoise.close_connections()


async def init():
    """Init the database"""
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()
    try:
        await __create_superuser()
    finally:
        ...
