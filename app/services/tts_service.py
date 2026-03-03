from __future__ import annotations

import uuid
from pathlib import Path

import requests

from app.config import get_settings

settings = get_settings()


class TTSServiceError(Exception):
    pass


class TTSService:
    def __init__(self) -> None:
        self.base_url = settings.elevenlabs_base_url.rstrip("/")
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id
        self.model_id = settings.elevenlabs_model_id
        settings.media_path.mkdir(parents=True, exist_ok=True)

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def synthesize(self, text: str) -> str:
        if not self.configured:
            raise TTSServiceError("ELEVENLABS_API_KEY no configurada")

        url = f"{self.base_url}/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        payload = {
            "text": text[:3000],
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
        except requests.RequestException as exc:
            raise TTSServiceError(f"Error de red llamando ElevenLabs: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text[:500]
            raise TTSServiceError(f"ElevenLabs respondió {response.status_code}: {detail}")

        filename = f"tts_{uuid.uuid4().hex}.mp3"
        filepath = Path(settings.media_dir) / filename
        filepath.write_bytes(response.content)
        return f"{settings.media_url_prefix}/{filename}"
