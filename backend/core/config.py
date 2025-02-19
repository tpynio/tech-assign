from pydantic_settings import BaseSettings
from os import getenv


class Settings(BaseSettings):
    class Config:
        env_prefix = "APP_"

    # Swagger settings
    TITLE: str = "Tech-assign backend"
    OPENAPI_PREFIX: str = ""
    ROOT_PATH: str = ""

    # LOG settings
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = ""

    # BACK settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # DB MySQL settings
    MYSQL_URL: str = "mysql+asyncmy://user:password@localhost:3307/database"
    ECHO: bool = False
    MAX_OVERFLOW: int = 10
    POOL_SIZE: int = 10
    BATCH_SIZE: int = 15

    # DB Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_LOCK_PREFIX: str = "lock_prefix"
    REDIS_KEY_PREFIX: str = "key_prefix"
    REDIS_EXPIRE: int = 86400

    # AUTH settings
    COOKIE_SESSION_ID_KEY_NAME: str = "session_id"


ENV_FILE_IF_USED = getenv("USE_ENV_CONFIG") or getenv("ENV_FILE", ".env")
settings = Settings(_env_file=ENV_FILE_IF_USED)
