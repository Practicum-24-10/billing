from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    db_name: str = "bolshoy_db"
    db_user: str = "app"
    db_password: str = "123qwe"
    db_host: str = "localhost"
    db_port: str = "5432"


pg_config = PostgresConfig()
