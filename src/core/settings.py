from os import environ as env
from pathlib import Path

from pydantic import BaseModel, Field


class APISettings(BaseModel):
    host: str = Field(alias="UVICORN_HOST")
    port: int = Field(alias="UVICORN_PORT")


class DatabaseSettings(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db_name: str = Field(alias="POSTGRES_DB")

    @property
    def db_uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class LoggingSettings(BaseModel):
    log_level: str = Field(alias="LOG_LEVEL", default="DEBUG")
    log_file: str = Field(alias="LOG_FILE", default="app.log")
    log_encoding: str = Field(alias="LOG_ENCODING", default="utf-8")


class Settings(BaseModel):
    api: APISettings = Field(default_factory=lambda: APISettings(**env))
    database: DatabaseSettings = Field(default_factory=lambda: DatabaseSettings(**env))
    logging: LoggingSettings = Field(default_factory=lambda: LoggingSettings(**env))


def load_dotenv(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        return
    with path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":
                continue
            try:
                key, value = line.strip().split("=", maxsplit=1)
                env.setdefault(key, value)
            except ValueError:
                print(f"Invalid line in .env file: {line.strip()}")


load_dotenv(".env")
