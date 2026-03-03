Param(
    [string]$ZipName = "psicoasistente_mvp.zip"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$zipPath = Join-Path $root $ZipName

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

$items = @(
    "app",
    "frontend",
    "scripts",
    "requirements.txt",
    ".env.example",
    "README.md",
    "test_elevenlabs_tts.py"
)

Push-Location $root
try {
    Compress-Archive -Path $items -DestinationPath $zipPath -Force
    Write-Host "ZIP generado: $zipPath" -ForegroundColor Green
    Write-Host "Nota: /media, .env, .venv y __pycache__ quedan excluidos por diseño." -ForegroundColor Yellow
}
finally {
    Pop-Location
}
