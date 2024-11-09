from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 4000
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:3000 http://127.0.0.1:3000'

    REDIS_URL: RedisDsn = RedisDsn('redis://redis:6379/1')


settings = Settings()
