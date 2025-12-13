from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    YANDEX_GPT_API: str
    CATALOG_ID: str

settings = Settings()

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
DATABASE_URL = settings.DATABASE_URL
YANDEX_GPT_API = settings.YANDEX_GPT_API
CATALOG_ID = settings.CATALOG_ID
