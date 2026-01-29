Instalación y ejecución local

Este proyecto utiliza Python 3.11 y entorno virtual para aislar dependencias.

Requisitos

Verifica tu versión de Python:

python3 --version

Debe ser Python 3.11.

Crear entorno virtual
macOS / Linux
python3.11 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

Instalar dependencias
pip install -r requirements.txt

Ejecutar la aplicación

Desde la raíz del proyecto:

uvicorn app.main:app --reload

La API estará disponible en:

http://localhost:8000

http://localhost:8000/api/docs
