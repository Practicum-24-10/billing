import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

# from pydantic import BaseSettings
from backend.src.core.logger import LOGGING


class AppSettings(BaseSettings):
    project_name: str = "Some project name"
    redis_host: str = "localhost"
    redis_port: int = 6379
    logging_on: bool = True
    sentry_dsn: str = ""
    public_key: str = "jwt-key.pub"


config = AppSettings()

if config.logging_on:
    logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_KEY_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # type: ignore
PUBLIC_KEY = os.path.join(PUBLIC_KEY_DIR, config.public_key)  # type: ignore
