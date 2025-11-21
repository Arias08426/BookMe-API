from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Lee las variables de entorno del archivo .env
    """

    app_name: str = "BookMe API"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./bookme.db"
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia de Settings (singleton).
    Se cachea para no leer el archivo .env múltiples veces.
    """
    return Settings()
