import os
from cmath import log

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Configuration of application parameters
    """

    API_STR: str = ""
    SECRET_KEY: str = "d40ee10164eb364aeeedf632ac21ba77e1e27493259cd612e0a7d2ac2f04fbd2"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SLIDE_URL = (
        os.environ["SLIDE_URL"]
        if "SLIDE_URL" in os.environ
        else "http://127.0.0.1:8001"
    )

    DATABASE_URL = (
        os.environ["DATABASE_URL"]
        if "DATABASE_URL" in os.environ
        else "mysql+mysqlconnector://user:password@127.0.0.1/db?charset=utf8mb4"
    )

    RABBIT_URL = (
        os.environ["RABBIT_URL"]
        if "RABBIT_URL" in os.environ
        else "amqp://guest:guest@127.0.0.1:5672//"
    )

    MINIO_ROOT_USER = (
        os.environ["MINIO_ROOT_USER"] if "MINIO_ROOT_USER" in os.environ else "minio"
    )
    MINIO_ROOT_PASSWORD = (
        os.environ["MINIO_ROOT_PASSWORD"]
        if "MINIO_ROOT_PASSWORD" in os.environ
        else "minioKey1234"
    )

    MINIO_URL = os.environ["MINIO_URL"] if "MINIO_URL" in os.environ else "minio:9000"
    MINIO_SECURE = (
        os.environ["MINIO_SECURE"] if "MINIO_SECURE" is os.environ else "True"
    )

    FIRST_SUPERUSER_EMAIL: EmailStr = os.environ.get("LEARN_API_ADMIN_EMAIL", None)
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("LEARN_API_ADMIN_PASSWORD", None)
    FIRST_SUPERUSER_FIRSTNAME: str = os.environ.get("LEARN_API_ADMIN_FIRSTNAME", None)
    FIRST_SUPERUSER_LASTNAME: str = os.environ.get("LEARN_API_ADMIN_LASTNAME", None)
    USERS_OPEN_REGISTRATION: bool = True

    SENTRY_DSN = os.environ["SENTRY_DSN"] if "SENTRY_DSN" in os.environ else None
    SENTRY_ENVIRONMENT = (
        os.environ["SENTRY_ENVIRONMENT"]
        if "SENTRY_ENVIRONMENT" in os.environ
        else "production"
    )

    class Config:
        case_sensitive = True


settings = Settings()
