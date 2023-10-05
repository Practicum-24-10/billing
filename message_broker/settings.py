from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amqp_host: str = 'localhost'
    amqp_port: int = 5672
    def get_amqp_url(self) -> str:
        return f'amqp://{self.amqp_host}:{self.amqp_port}/'


settings = Settings()
