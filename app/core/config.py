from pydantic_settings import BaseSettings
import os

ENV = os.getenv("ENV", "production")  # default to development

class Settings(BaseSettings):
    app_name: str = "FastAPI Blog"
    database_url: str
    secret_key: str
    openweather_api_key: str
    environment: str = ENV
    algorithm: str = "HS256"

    class Config:
        env_file = f".env.{ENV}"  # loads .env.development or .env.production

settings = Settings()