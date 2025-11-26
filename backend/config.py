from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	DATABASE_URL: str = "sqlite:///./voxai.db"
	WEBHOOK_SECRET: str = "changeme"
	ENV: str = "local"
	
	model_config = SettingsConfigDict(
		env_file=".env",
		extra="ignore",
	)

settings = Settings()