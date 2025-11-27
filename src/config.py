# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model_name: str = "gemini-2.5-flash"
    serper_api_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# 匯出單例設定
settings = Settings()
