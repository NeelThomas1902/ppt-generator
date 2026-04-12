"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # API keys
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")

    # Demo / free-testing mode (no API key required)
    demo_mode: bool = Field(default=False, alias="DEMO_MODE")

    # App settings
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    debug: bool = Field(default=True, alias="DEBUG")

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./ppt_generator.db", alias="DATABASE_URL"
    )

    # File storage
    upload_dir: str = Field(default="uploads", alias="UPLOAD_DIR")
    templates_dir: str = Field(default="app/templates", alias="TEMPLATES_DIR")
    max_upload_size_mb: int = Field(default=50, alias="MAX_UPLOAD_SIZE_MB")

    # CORS
    allowed_origins_str: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        alias="ALLOWED_ORIGINS",
    )

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_str.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        populate_by_name = True


settings = Settings()
