 PsicoAsistente MVP (FastAPI + Frontend + ElevenLabs TTS)

Aplicación web full-stack con registro/login (JWT), chat con historial por usuario, respuestas de orientación general (psicoeducación segura) y síntesis de voz con ElevenLabs (texto + audio mp3).

> Disclaimer clínico (obligatorio): Esto no sustituye terapia profesional. Si estás en crisis o en peligro, busca ayuda profesional o servicios de emergencia de tu país.

---

 1) Requisitos

- Windows 10/11
- Python 3.11+ (recomendado 3.11 o 3.12)
- PowerShell
- Cuenta/API key de ElevenLabs (opcional para texto, requerida para audio)

---

 2) Estructura del proyecto

```text
project_root/
 ├─ app/
 │  ├─ main.py
 │  ├─ config.py
 │  ├─ database.py
 │  ├─ models.py
 │  ├─ schemas.py
 │  ├─ security.py
 │  ├─ routers/
 │  │  ├─ auth.py
 │  │  ├─ chat.py
 │  │  └─ tts.py
 │  └─ services/
 │ 	├─ assistant_engine.py
 │ 	└─ tts_service.py
 ├─ frontend/
 │  ├─ index.html
 │  ├─ chat.html
 │  ├─ styles.css
 │  └─ app.js
 ├─ media/
 ├─ scripts/
 │  ├─ run_backend.ps1
 │  ├─ run_backend.cmd
 │  └─ make_zip.ps1
 ├─ requirements.txt
 ├─ .env.example
 ├─ test_elevenlabs_tts.py
 └─ README.md

```
3) Instalación (Windows PowerShell)

Paso 1: Entrar al proyecto

powershell
cd C:\ruta\a\project_root


Paso 2: Crear entorno virtual

powershell
python -m venv .venv

Paso 3: Activar entorno virtual

powershell
.\.venv\Scripts\Activate.ps1


Si PowerShell bloquea scripts temporalmente:

powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1


Paso 4: Instalar dependencias

powershell
python -m pip install --upgrade pip
pip install -r .\requirements.txt


text
Successfully installed fastapi ... uvicorn ... sqlalchemy ...


Paso 5: Crear `.env` desde `.env.example`

powershell
Copy-Item .\.env.example .\.env
notepad .\.env


Edita estos valores:
- `ELEVENLABS_API_KEY=...` (si quieres audio real)
- `SECRET_KEY=...` (cadena larga y aleatoria)
- `DATABASE_URL=sqlite:///./app.db` (o PostgreSQL)

Paso 6: Ejecutar backend

powershell
.\scripts\run_backend.ps1


text
Iniciando backend FastAPI en http://127.0.0.1:8000 ...
INFO:     Will watch for changes in these directories: ['C:\...\project_root']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Application startup complete.

4) Abrir la UI en navegador

- Login/registro: `http://127.0.0.1:8000/`
- Chat: `http://127.0.0.1:8000/chat`

- `/` muestra formularios de registro/login + disclaimer visible.
- `/chat` pide token (si no has iniciado sesión redirige a `/`).

---

5) Flujo de prueba manual (registro → login → chat → audio)

1. Ve a `http://127.0.0.1:8000/`
2. Regístrate con email y contraseña (mín. 8)
3. Redirección automática a `/chat`
4. Envía un mensaje como: `Me siento muy ansioso hoy`
5. Debes ver:
   - respuesta en texto
   - disclaimer incluido
   - `audio_url` en metadata (si TTS está configurado)
   - intento de reproducción automática de audio

- Mensaje del asistente con sugerencia de respiración guiada.
- Si ElevenLabs está bien configurado, se escucha voz y el navegador hace streaming del mp3 desde `/media/...mp3`.
- Si falla TTS, el chat sigue funcionando con texto y muestra `audio_error`.

---

6) Probar endpoints (PowerShell)

6.1 Health

powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"

6.2 Registro

powershell
$registerBody = @{
  email = "demo@example.com"
  password = "ClaveSegura123!"
  full_name = "Demo"
} | ConvertTo-Json

$reg = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/auth/register" -ContentType "application/json" -Body $registerBody
$reg


6.3 Login (anti-enumeración)

powershell
$loginBody = @{
  email = "demo@example.com"
  password = "ClaveSegura123!"
} | ConvertTo-Json

$login = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/auth/login" -ContentType "application/json" -Body $loginBody
$token = $login.access_token
$token


6.4 /auth/me

powershell
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/auth/me" -Headers $headers


6.5 Enviar mensaje al chat

powershell
$chatBody = @{ message = "Tengo ansiedad y no puedo dormir" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/chat/message" -Headers $headers -ContentType "application/json" -Body $chatBody


6.6 Mensaje de crisis (prueba de seguridad)

powershell
$chatBody = @{ message = "No quiero vivir" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/chat/message" -Headers $headers -ContentType "application/json" -Body $chatBody


6.7 TTS directo (opcional, protegido con JWT)

powershell
$ttsBody = @{ text = "Hola, esta es una prueba de audio" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/tts" -Headers $headers -ContentType "application/json" -Body $ttsBody


---

 7) Probar TTS con script aislado (`test_elevenlabs_tts.py`)

powershell
python .\test_elevenlabs_tts.py --text "Hola, prueba de ElevenLabs" --voice-id EXAVITQu4vr4xnSDxMaL


8) Base de datos PostgreSQL (opcional)

Cambia `DATABASE_URL` en `.env`, por ejemplo:

env
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/psico_db


Luego instala driver adicional:

powershell
pip install psycopg2-binary


---

 9) Seguridad implementada (resumen)

- Variables de entorno (`.env`) para secretos y API keys
- Password hashing con Passlib (`bcrypt_sha256`)
- JWT con `python-jose`
- Anti-enumeración en login (mismo error)
- Manejo de errores 422/401/409/500 con JSON
- Disclaimer visible en UI y en respuestas
- Respuesta de crisis con `safety_flag="CRISIS"`
- Sin diagnóstico ni medicación

---

 10) Generar ZIP (sin incluir `.env` real ni claves)

 Opción recomendada (script)

powershell
.\scripts\make_zip.ps1

Opción manual con `Compress-Archive` (exacta)

powershell
Compress-Archive -Path app,frontend,scripts,requirements.txt,.env.example,README.md,test_elevenlabs_tts.py -DestinationPath .\psicoasistente_mvp.zip -Force