import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str
    VERSION: str

    # SSH
    SSH_HOST: str
    SSH_PORT: int
    SSH_USERNAME: str
    SSH_PASSWORD: str

    # MongoDB
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_DATABASE_NAME: str
    MONGODB_HOST: str
    MONGODB_TUNNEL_PORT: int
    MONGODB_USE_TLS: bool
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int = 7
    REDIS_TTL: int = 3600 # 1 hour


    #log
    LOG_FILE: str = "logs/api.log"

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'dev')}"


settings = Settings()







