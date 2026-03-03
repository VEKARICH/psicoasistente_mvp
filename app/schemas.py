from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class ErrorResponse(BaseModel):
    detail: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: UserOut


class ChatMessageIn(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatMessageOut(BaseModel):
    reply_text: str
    audio_url: str | None
    audio_error: str | None = None
    disclaimer: str
    safety_flag: str | None = None
    intent: str | None = None


class ChatHistoryItem(BaseModel):
    id: int
    role: str
    content: str
    intent: str | None = None
    safety_flag: str | None = None
    audio_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=3000)


class TTSResponse(BaseModel):
    audio_url: str | None
    audio_error: str | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    tts_configured: bool
