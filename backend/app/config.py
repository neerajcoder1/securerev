import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "securerev")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "securerev_dev_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "securerev")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres") # defaults to docker-compose service name
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
