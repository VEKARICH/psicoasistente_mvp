from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, chat, tts

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")

# Crear tablas (MVP). En producción usar migraciones (Alembic).
Base.metadata.create_all(bind=engine)

# Asegurar directorios
Path(settings.media_dir).mkdir(parents=True, exist_ok=True)
Path(settings.frontend_dir).mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación en la solicitud.",
            "errors": exc.errors(),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "path": str(request.url.path)})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor.",
            "path": str(request.url.path),
        },
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "tts_configured": settings.tts_configured,
    }


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tts.router)


@app.get("/")
def root_ui():
    index_file = Path(settings.frontend_dir) / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=500, detail="Frontend no encontrado (index.html).")
    return FileResponse(index_file)


@app.get("/chat")
def chat_ui():
    chat_file = Path(settings.frontend_dir) / "chat.html"
    if not chat_file.exists():
        raise HTTPException(status_code=500, detail="Frontend no encontrado (chat.html).")
    return FileResponse(chat_file)


app.mount("/frontend", StaticFiles(directory=settings.frontend_dir), name="frontend")
app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")
