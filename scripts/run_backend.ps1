Param(
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "No existe .venv. Crea el entorno virtual primero." -ForegroundColor Red
    exit 1
}

Write-Host "Iniciando backend FastAPI en http://$BindHost`:$Port ..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host $BindHost --port $Port --reload
