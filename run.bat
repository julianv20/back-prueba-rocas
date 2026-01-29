@echo off
echo Activando entorno virtual y ejecutando la API...
call venv\Scripts\activate.bat
echo.
echo Entorno virtual activado!
echo.
echo Opciones:
echo   1. Ejecutar API (uvicorn app.main:app --reload)
echo   2. Poblar base de datos (python seed_data.py)
echo   3. Ejecutar tests (pytest -v)
echo   4. Salir
echo.
set /p option="Selecciona una opcion (1-4): "

if "%option%"=="1" (
    echo.
    echo Ejecutando API en http://localhost:8000...
    echo Documentacion en http://localhost:8000/api/docs
    echo.
    uvicorn app.main:app --reload
) else if "%option%"=="2" (
    echo.
    echo Poblando base de datos...
    python seed_data.py
    echo.
    pause
) else if "%option%"=="3" (
    echo.
    echo Ejecutando tests...
    pytest -v
    echo.
    pause
) else (
    exit
)
