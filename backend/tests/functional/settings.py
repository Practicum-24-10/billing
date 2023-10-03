from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    service_url: str = "http://localhost:8000/api/v1/"


test_settings = TestSettings()
