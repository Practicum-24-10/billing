import gettext

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    language: str = "str"

    model_config = SettingsConfigDict(
        env_file="admin/.env", env_file_encoding="utf-8", extra="ignore"
    )


class PgSettings(BaseSettings):
    db_name: str = "str"
    db_user: str = "str"
    db_password: str = "str"
    db_host: str = "str"
    db_port: int = 111

    model_config = SettingsConfigDict(
        env_file="admin/.env", env_file_encoding="utf-8", extra="ignore"
    )


app_config = AppSettings()
pg_config = PgSettings()


language_translation = gettext.translation(
    "base", "admin/locales", languages=[app_config.language]
)
translation = language_translation.gettext
