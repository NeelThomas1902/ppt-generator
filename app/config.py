from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ppt-generator"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "sqlite:///./ppt_generator.db"

    anthropic_api_key: str = ""

    upload_dir: str = "uploads"
    output_dir: str = "outputs"
    max_file_size_mb: int = 50

    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
