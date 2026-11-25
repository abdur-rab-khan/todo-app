from fastapi._compat.v2 import ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: str
    user: str
    db_name: str
    host_name: str
    password: str

    model_config = {"env_file": ".env"}


settings = Settings()
