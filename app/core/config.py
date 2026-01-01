from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    APP_NAME: str
    # PostgreSQL 
    POSTGRES_URL: str
    # Oracle 
    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_DSN: str
    # Logging
    LOG_LEVEL: str
    # JWT
    JWT_SECRET_KEY: str
    ISSUER: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    # LDAP
    LDAP_SERVER: str
    LDAP_PORT: int
    LDAP_BASE_DN: str
    LDAP_TIMEOUT: int
    # Pydantic Settings 
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()