from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_username: str  
    database_password: str 
    database_hostname: str 
    database_port: str 
    database_name: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file = BASE_DIR / ".env")

settings = Settings()

