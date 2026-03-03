from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import ChatMessage, User
from app.schemas import ChatHistoryItem, ChatMessageIn, ChatMessageOut
from app.security import get_current_user
from app.services.assistant_engine import generate_safe_reply
from app.services.tts_service import TTSService, TTSServiceError

router = APIRouter(prefix="/chat", tags=["chat"])
settings = get_settings()


@router.get("/history", response_model=list[ChatHistoryItem])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        .limit(200)
        .all()
    )
    return rows


@router.post("/message", response_model=ChatMessageOut)
def chat_message(payload: ChatMessageIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_msg = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=payload.message.strip(),
    )
    db.add(user_msg)
    db.commit()

    # Historial ligero para futura integración con LLM (últimos 20 mensajes)
    recent = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
        .limit(20)
        .all()
    )
    history = [
        {"role": m.role, "content": m.content, "intent": m.intent, "safety_flag": m.safety_flag}
        for m in reversed(recent)
    ]

    assistant_reply = generate_safe_reply(payload.message, history=history)

    tts = TTSService()
    audio_url = None
    audio_error = None
    try:
        audio_url = tts.synthesize(assistant_reply.reply_text)
    except TTSServiceError as exc:
        audio_error = str(exc)

    assistant_msg = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=assistant_reply.reply_text,
        intent=assistant_reply.intent,
        safety_flag=assistant_reply.safety_flag,
        audio_url=audio_url,
    )
    db.add(assistant_msg)
    db.commit()

    return ChatMessageOut(
        reply_text=assistant_reply.reply_text,
        audio_url=audio_url,
        audio_error=audio_error,
        disclaimer=settings.disclaimer_text,
        safety_flag=assistant_reply.safety_flag,
        intent=assistant_reply.intent,
    )
