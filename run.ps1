# Script de inicio para PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Stock API - Inicio Rápido" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# Menú de opciones
Write-Host "Opciones disponibles:" -ForegroundColor Cyan
Write-Host "  1. Ejecutar API (uvicorn)" -ForegroundColor White
Write-Host "  2. Poblar base de datos (seed_data.py)" -ForegroundColor White
Write-Host "  3. Ejecutar tests (pytest)" -ForegroundColor White
Write-Host "  4. Instalar dependencias" -ForegroundColor White
Write-Host "  5. Salir" -ForegroundColor White
Write-Host ""

$option = Read-Host "Selecciona una opción (1-5)"

switch ($option) {
    "1" {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Ejecutando API..." -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "URL: http://localhost:8000" -ForegroundColor Yellow
        Write-Host "Docs: http://localhost:8000/api/docs" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Gray
        Write-Host ""
        uvicorn app.main:app --reload
    }
    "2" {
        Write-Host ""
        Write-Host "Poblando base de datos con datos de prueba..." -ForegroundColor Yellow
        python seed_data.py
        Write-Host ""
        Write-Host "✓ Base de datos poblada correctamente" -ForegroundColor Green
        Read-Host "Presiona Enter para continuar"
    }
    "3" {
        Write-Host ""
        Write-Host "Ejecutando tests..." -ForegroundColor Yellow
        pytest -v
        Write-Host ""
        Read-Host "Presiona Enter para continuar"
    }
    "4" {
        Write-Host ""
        Write-Host "Instalando dependencias..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host ""
        Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
        Read-Host "Presiona Enter para continuar"
    }
    default {
        Write-Host "Saliendo..." -ForegroundColor Gray
        exit
    }
}
