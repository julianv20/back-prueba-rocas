# Instalación y ejecución local

Este proyecto utiliza Python 3.11 y entorno virtual para aislar dependencias.

## Requisitos

Verifica tu versión de Python:

```bash
python3 --version
Debe ser Python 3.11 o superior.

Crear entorno virtual
macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
Windows
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
Instalar dependencias
pip install -r requirements.txt
Ejecutar la aplicación
Desde la raíz del proyecto:

IMPORTANTE ejecutar esto:
python seed_data.py
para llenar db

uvicorn app.main:app --reload
La API estará disponible en:

http://localhost:8000
http://localhost:8000/api/docs

