from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PsicoAsistente MVP"
    debug: bool = False
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = Field("sqlite:///./app.db", alias="DATABASE_URL")

    elevenlabs_api_key: str | None = Field(default=None, alias="ELEVENLABS_API_KEY")
    elevenlabs_voice_id: str = Field(default="EXAVITQu4vr4xnSDxMaL", alias="ELEVENLABS_VOICE_ID")
    elevenlabs_model_id: str = Field(default="eleven_multilingual_v2", alias="ELEVENLABS_MODEL_ID")
    elevenlabs_base_url: str = Field(default="https://api.elevenlabs.io", alias="ELEVENLABS_BASE_URL")

    media_dir: str = "media"
    media_url_prefix: str = "/media"
    frontend_dir: str = "frontend"

    disclaimer_text: str = (
        "Esto no sustituye terapia profesional. Si estás en crisis o en peligro, "
        "busca ayuda profesional o servicios de emergencia de tu país."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def media_path(self) -> Path:
        return Path(self.media_dir)

    @property
    def frontend_path(self) -> Path:
        return Path(self.frontend_dir)

    @property
    def tts_configured(self) -> bool:
        return bool(self.elevenlabs_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
