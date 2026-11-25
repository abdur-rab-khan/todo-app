from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    port: str = Field(validation_alias="PORT")
    user: str = Field(validation_alias="USER")
    db_name: str = Field(validation_alias="DATABASE_NAME")
    host_name: str = Field(validation_alias="HOST_NAME")
    password: str = Field(validation_alias="PASSWORD")

    model_config = {"env_file": ".env"}

    @property
    def database_url(self) -> str:
        """Single source of truth for the database connection string.

        Both the runtime engine and Alembic's env.py consume this, so the
        credentials are never duplicated (or committed) in alembic.ini.
        """
        return URL.create(
            "postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host_name,
            port=int(self.port),
            database=self.db_name,
        ).render_as_string(hide_password=False)


settings = Settings()
