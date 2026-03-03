from fastapi import APIRouter, Depends

from app.schemas import TTSRequest, TTSResponse
from app.security import get_current_user
from app.services.tts_service import TTSService, TTSServiceError

router = APIRouter(prefix="/tts", tags=["tts"])


@router.post("", response_model=TTSResponse)
def synthesize_tts(payload: TTSRequest, _current_user=Depends(get_current_user)):
    service = TTSService()
    try:
        url = service.synthesize(payload.text)
        return TTSResponse(audio_url=url)
    except TTSServiceError as exc:
        return TTSResponse(audio_url=None, audio_error=str(exc))
