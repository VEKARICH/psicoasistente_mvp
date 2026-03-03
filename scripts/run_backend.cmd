@echo off
IF NOT EXIST .venv\Scripts\python.exe (
  echo No existe .venv. Crea el entorno virtual primero.
  exit /b 1
)

echo Iniciando backend FastAPI en http://127.0.0.1:8000 ...
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
