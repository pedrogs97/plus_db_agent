import os

from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_HOST = os.getenv("POSTGRESQL_HOST", "localhost")


def get_database_url(test=False, sqlite=False):
    """Return database url"""
    if sqlite:
        return "sqlite://db.sqlite3"
    server = DB_HOST if not test else os.getenv("POSTGRESQL_HOST_TEST", "localhost")
    db = os.getenv("POSTGRESQL_DATABASE", "app") if not test else "db_test"
    user = (
        os.getenv("POSTGRESQL_USER", "root")
        if not test
        else os.getenv("POSTGRESQL_USER_TEST", "root")
    )
    password = (
        os.getenv("POSTGRESQL_PASSWORD", "")
        if not test
        else os.getenv("POSTGRESQL_PASSWORD_TEST", "")
    )
    port = os.getenv("POSTGRESQL_PORT", "5432")
    return f"postgres://{user}:{password}@{server}:{port}/{db}"


DATABASE_CONFIG = {
    "connections": {"default": get_database_url(sqlite=os.getenv("ENABLE_SQLITE"))},
    "apps": {
        "core": {
            "models": [
                "aerich.models",
                "plus_db_agent.models",
            ],
            "default_connection": "default",
        },
    },
}

DEFAULT_DATE_FORMAT = "%d/%m/%Y"
DEFAULT_DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
