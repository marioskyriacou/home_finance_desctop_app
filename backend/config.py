"""
read settings from.env file.
The .env file will not commited to GitHub
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
	app_name: str = "Finance App"

	db_host: str = "localhost"
	db_port: int = 5432
	db_name: str
	db_user: str
	db_password: str

	secret_key: str
	access_token_expire_minutes: int = 60

	# tell to a class how to automatically read and parse variables from an external .env file.
	model_config = SettingsConfigDict(
		env_file= BASE_DIR / ".env",
		env_file_encoding="utf-8",
		extra = "ignore"
	)

settings=Settings()