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
D:.
├───.venv
│   ├───Include
│   │   └───site
│   │       └───python3.12
│   │           └───greenlet
│   ├───Lib
│   │   └───site-packages
│   │       ├───annotated_types
│   │       │   └───__pycache__
│   │       ├───annotated_types-0.7.0.dist-info
│   │       │   └───licenses
│   │       ├───anyio
│   │       │   ├───abc
│   │       │   │   └───__pycache__
│   │       │   ├───streams
│   │       │   │   └───__pycache__
│   │       │   ├───_backends
│   │       │   │   └───__pycache__
│   │       │   ├───_core
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───anyio-4.12.1.dist-info
│   │       │   └───licenses
│   │       ├───bcrypt
│   │       │   └───__pycache__
│   │       ├───bcrypt-4.1.3.dist-info
│   │       ├───certifi
│   │       │   └───__pycache__
│   │       ├───certifi-2026.1.4.dist-info
│   │       │   └───licenses
│   │       ├───cffi
│   │       │   └───__pycache__
│   │       ├───cffi-2.0.0.dist-info
│   │       │   └───licenses
│   │       ├───charset_normalizer
│   │       │   ├───cli
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───charset_normalizer-3.4.4.dist-info
│   │       │   └───licenses
│   │       ├───click
│   │       │   └───__pycache__
│   │       ├───click-8.3.1.dist-info
│   │       │   └───licenses
│   │       ├───colorama
│   │       │   ├───tests
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───colorama-0.4.6.dist-info
│   │       │   └───licenses
│   │       ├───cryptography
│   │       │   ├───hazmat
│   │       │   │   ├───asn1
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───backends
│   │       │   │   │   ├───openssl
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───bindings
│   │       │   │   │   ├───openssl
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───_rust
│   │       │   │   │   │   └───openssl
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───decrepit
│   │       │   │   │   ├───ciphers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───primitives
│   │       │   │   │   ├───asymmetric
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───ciphers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───kdf
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───serialization
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───twofactor
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───x509
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───cryptography-46.0.5.dist-info
│   │       │   └───licenses
│   │       ├───dns
│   │       │   ├───dnssecalgs
│   │       │   │   └───__pycache__
│   │       │   ├───quic
│   │       │   │   └───__pycache__
│   │       │   ├───rdtypes
│   │       │   │   ├───ANY
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───CH
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───IN
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───dnspython-2.8.0.dist-info
│   │       │   └───licenses
│   │       ├───dotenv
│   │       │   └───__pycache__
│   │       ├───ecdsa
│   │       │   └───__pycache__
│   │       ├───ecdsa-0.19.1.dist-info
│   │       ├───email_validator
│   │       │   └───__pycache__
│   │       ├───email_validator-2.2.0.dist-info
│   │       ├───fastapi
│   │       │   ├───dependencies
│   │       │   │   └───__pycache__
│   │       │   ├───middleware
│   │       │   │   └───__pycache__
│   │       │   ├───openapi
│   │       │   │   └───__pycache__
│   │       │   ├───security
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───fastapi-0.116.1.dist-info
│   │       │   └───licenses
│   │       ├───greenlet
│   │       │   ├───platform
│   │       │   │   └───__pycache__
│   │       │   ├───tests
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───greenlet-3.3.2.dist-info
│   │       │   └───licenses
│   │       ├───h11
│   │       │   └───__pycache__
│   │       ├───h11-0.16.0.dist-info
│   │       │   └───licenses
│   │       ├───httptools
│   │       │   ├───parser
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───httptools-0.7.1.dist-info
│   │       │   └───licenses
│   │       ├───idna
│   │       │   └───__pycache__
│   │       ├───idna-3.11.dist-info
│   │       │   └───licenses
│   │       ├───jose
│   │       │   ├───backends
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───multipart
│   │       │   └───__pycache__
│   │       ├───passlib
│   │       │   ├───crypto
│   │       │   │   ├───scrypt
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───_blowfish
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───ext
│   │       │   │   ├───django
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───handlers
│   │       │   │   └───__pycache__
│   │       │   ├───tests
│   │       │   │   └───__pycache__
│   │       │   ├───utils
│   │       │   │   ├───compat
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───_data
│   │       │   │   └───wordsets
│   │       │   └───__pycache__
│   │       ├───passlib-1.7.4.dist-info
│   │       ├───pip
│   │       │   ├───_internal
│   │       │   │   ├───cli
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───commands
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distributions
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───index
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───locations
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───metadata
│   │       │   │   │   ├───importlib
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───models
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───network
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───operations
│   │       │   │   │   ├───build
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───install
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───req
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───resolution
│   │       │   │   │   ├───legacy
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───resolvelib
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───utils
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───vcs
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───_vendor
│   │       │   │   ├───cachecontrol
│   │       │   │   │   ├───caches
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───certifi
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───dependency_groups
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distlib
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distro
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───idna
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───msgpack
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───packaging
│   │       │   │   │   ├───licenses
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pkg_resources
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───platformdirs
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pygments
│   │       │   │   │   ├───filters
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───formatters
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───lexers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───styles
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pyproject_hooks
│   │       │   │   │   ├───_in_process
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───requests
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───resolvelib
│   │       │   │   │   ├───resolvers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───rich
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───tomli
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───tomli_w
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───truststore
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───urllib3
│   │       │   │   │   ├───contrib
│   │       │   │   │   │   ├───_securetransport
│   │       │   │   │   │   │   └───__pycache__
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───packages
│   │       │   │   │   │   ├───backports
│   │       │   │   │   │   │   └───__pycache__
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───util
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pip-26.0.1.dist-info
│   │       │   └───licenses
│   │       │       └───src
│   │       │           └───pip
│   │       │               └───_vendor
│   │       │                   ├───cachecontrol
│   │       │                   ├───certifi
│   │       │                   ├───dependency_groups
│   │       │                   ├───distlib
│   │       │                   ├───distro
│   │       │                   ├───idna
│   │       │                   ├───msgpack
│   │       │                   ├───packaging
│   │       │                   ├───pkg_resources
│   │       │                   ├───platformdirs
│   │       │                   ├───pygments
│   │       │                   ├───pyproject_hooks
│   │       │                   ├───requests
│   │       │                   ├───resolvelib
│   │       │                   ├───rich
│   │       │                   ├───tomli
│   │       │                   ├───tomli_w
│   │       │                   ├───truststore
│   │       │                   └───urllib3
│   │       ├───pyasn1
│   │       │   ├───codec
│   │       │   │   ├───ber
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───cer
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───der
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───native
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───compat
│   │       │   │   └───__pycache__
│   │       │   ├───type
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pyasn1-0.6.2.dist-info
│   │       │   └───licenses
│   │       ├───pycparser
│   │       │   └───__pycache__
│   │       ├───pycparser-3.0.dist-info
│   │       │   └───licenses
│   │       ├───pydantic
│   │       │   ├───deprecated
│   │       │   │   └───__pycache__
│   │       │   ├───experimental
│   │       │   │   └───__pycache__
│   │       │   ├───plugin
│   │       │   │   └───__pycache__
│   │       │   ├───v1
│   │       │   │   └───__pycache__
│   │       │   ├───_internal
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pydantic-2.11.7.dist-info
│   │       │   └───licenses
│   │       ├───pydantic_core
│   │       │   └───__pycache__
│   │       ├───pydantic_core-2.33.2.dist-info
│   │       │   └───licenses
│   │       ├───pydantic_settings
│   │       │   ├───sources
│   │       │   │   ├───providers
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pydantic_settings-2.10.1.dist-info
│   │       │   └───licenses
│   │       ├───python_dotenv-1.1.1.dist-info
│   │       │   └───licenses
│   │       ├───python_jose-3.5.0.dist-info
│   │       │   └───licenses
│   │       ├───python_multipart
│   │       │   └───__pycache__
│   │       ├───python_multipart-0.0.20.dist-info
│   │       │   └───licenses
│   │       ├───pyyaml-6.0.3.dist-info
│   │       │   └───licenses
│   │       ├───requests
│   │       │   └───__pycache__
│   │       ├───requests-2.32.4.dist-info
│   │       │   └───licenses
│   │       ├───rsa
│   │       │   └───__pycache__
│   │       ├───rsa-4.9.1.dist-info
│   │       ├───six-1.17.0.dist-info
│   │       ├───sqlalchemy
│   │       │   ├───connectors
│   │       │   │   └───__pycache__
│   │       │   ├───cyextension
│   │       │   │   └───__pycache__
│   │       │   ├───dialects
│   │       │   │   ├───mssql
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───mysql
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───oracle
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───postgresql
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───sqlite
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───engine
│   │       │   │   └───__pycache__
│   │       │   ├───event
│   │       │   │   └───__pycache__
│   │       │   ├───ext
│   │       │   │   ├───asyncio
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───declarative
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───mypy
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───future
│   │       │   │   └───__pycache__
│   │       │   ├───orm
│   │       │   │   └───__pycache__
│   │       │   ├───pool
│   │       │   │   └───__pycache__
│   │       │   ├───sql
│   │       │   │   └───__pycache__
│   │       │   ├───testing
│   │       │   │   ├───fixtures
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───plugin
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───suite
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───util
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───sqlalchemy-2.0.43.dist-info
│   │       │   └───licenses
│   │       ├───starlette
│   │       │   ├───middleware
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───starlette-0.47.3.dist-info
│   │       │   └───licenses
│   │       ├───typing_extensions-4.15.0.dist-info
│   │       │   └───licenses
│   │       ├───typing_inspection
│   │       │   └───__pycache__
│   │       ├───typing_inspection-0.4.2.dist-info
│   │       │   └───licenses
│   │       ├───urllib3
│   │       │   ├───contrib
│   │       │   │   ├───emscripten
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───http2
│   │       │   │   └───__pycache__
│   │       │   ├───util
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───urllib3-2.6.3.dist-info
│   │       │   └───licenses
│   │       ├───uvicorn
│   │       │   ├───lifespan
│   │       │   │   └───__pycache__
│   │       │   ├───loops
│   │       │   │   └───__pycache__
│   │       │   ├───middleware
│   │       │   │   └───__pycache__
│   │       │   ├───protocols
│   │       │   │   ├───http
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───websockets
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───supervisors
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───uvicorn-0.35.0.dist-info
│   │       │   └───licenses
│   │       ├───watchfiles
│   │       │   └───__pycache__
│   │       ├───watchfiles-1.1.1.dist-info
│   │       │   └───licenses
│   │       ├───websockets
│   │       │   ├───asyncio
│   │       │   │   └───__pycache__
│   │       │   ├───extensions
│   │       │   │   └───__pycache__
│   │       │   ├───legacy
│   │       │   │   └───__pycache__
│   │       │   ├───sync
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───websockets-16.0.dist-info
│   │       │   └───licenses
│   │       ├───yaml
│   │       │   └───__pycache__
│   │       ├───_yaml
│   │       │   └───__pycache__
│   │       └───__pycache__
│   └───Scripts
├───app
│   ├───routers
│   │   └───__pycache__
│   ├───services
│   │   └───__pycache__
│   └───__pycache__
├───frontend
├───media
└───scripts
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