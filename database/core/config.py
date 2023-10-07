from pydantic import Field
from pydantic_settings import BaseSettings


class MainSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PostgresConfig(MainSettings):
    db_name: str = Field("billing_db", env="DB_NAME")
    db_user: str = Field("app", env="DB_USER")
    db_password: str = Field(" ", env="DB_PASSWORD")
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: str = Field("5432", env="DB_PORT")


pg_config = PostgresConfig()
