from pydantic_settings import BaseSettings
from os import getenv


class Settings(BaseSettings):
    class Config:
        env_prefix = "APP_"

    TITLE: str = "Tech-assign master backend"
    OPENAPI_PREFIX: str = ""
    ROOT_PATH: str = ""

    LOG_LEVEL: str = "DEBUG"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    MYSQL_ADDR: str = "mysql+asyncmy://user:password@localhost:3307/database"


ENV_FILE_IF_USED = getenv("USE_ENV_CONFIG") or getenv("ENV_FILE", ".env.local")
settings = Settings(_env_file=ENV_FILE_IF_USED)
