from pydantic_settings import BaseSettings
from os import getenv


class Settings(BaseSettings):
    class Config:
        env_prefix = "APP_"

    # Swagger settings
    TITLE: str = "Tech-assign master backend"
    OPENAPI_PREFIX: str = ""
    ROOT_PATH: str = ""

    # LOG settings
    LOG_LEVEL: str = "DEBUG"

    # BACK settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # DB settings
    MYSQL_ADDR: str = "mysql+asyncmy://user:password@localhost:3307/database"
    ECHO: bool = False
    MAX_OVERFLOW: int = 10
    POOL_SIZE: int = 10

    # AUTH settings
    COOKIE_SESSION_ID_KEY_NAME: str = "session_id"


ENV_FILE_IF_USED = getenv("USE_ENV_CONFIG") or getenv("ENV_FILE", ".env.local")
settings = Settings(_env_file=ENV_FILE_IF_USED)
