# 🚀 Guía de Inicio Rápido - Stock API

## Paso 1: Instalar Python

Asegúrate de tener **Python 3.11 o superior** instalado:

```powershell
python --version
```

Si no lo tienes, descárgalo de: https://www.python.org/downloads/

## Paso 2: Crear Entorno Virtual

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

Si encuentras error de permisos, ejecuta esto primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Paso 3: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias:
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT
- etc.

## Paso 4: Poblar Base de Datos

Ejecuta el script para crear datos de prueba:

```powershell
python seed_data.py
```

Esto creará:
- ✅ 2 usuarios de prueba
- ✅ 5 productos
- ✅ 3 bodegas
- ✅ 10 movimientos de stock

## Paso 5: Ejecutar la API

```powershell
uvicorn app.main:app --reload
```

Verás algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Paso 6: Probar la API

### Opción 1: Swagger UI (Recomendado)

Abre tu navegador y ve a:
```
http://localhost:8000/api/docs
```

Aquí podrás:
- Ver todos los endpoints
- Probar las peticiones
- Ver las respuestas

### Opción 2: Probar con cURL

#### 1. Login
```powershell
curl -X POST "http://localhost:8000/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"admin@example.com\",\"password\":\"admin123\"}'
```

Copia el `token` de la respuesta.

#### 2. Obtener Movimientos de Stock
```powershell
curl -X GET "http://localhost:8000/stock-moves?page=1&pageSize=10" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

#### 3. Obtener un Movimiento Específico
```powershell
curl -X GET "http://localhost:8000/stock-moves/SM001" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

#### 4. Actualizar Referencia
```powershell
curl -X PATCH "http://localhost:8000/stock-moves/SM001" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"reference\":\"Nueva referencia actualizada\"}'
```

## Usuarios de Prueba

### Admin
- **Email**: admin@example.com
- **Password**: admin123

### Test User
- **Email**: test@example.com
- **Password**: test123

## Endpoints Disponibles

### Autenticación (Sin token)
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión

### Stock Moves (Requiere token)
- `GET /stock-moves` - Listar movimientos (con filtros y paginación)
- `GET /stock-moves/{id}` - Obtener movimiento por ID
- `PATCH /stock-moves/{id}` - Actualizar referencia

### Health Check
- `GET /` - Estado de la API
- `GET /health` - Health check detallado

## Filtros Disponibles

Al hacer GET `/stock-moves`, puedes usar estos filtros:

```
?page=1                      # Número de página (default: 1)
&pageSize=10                 # Items por página (default: 10, max: 100)
&product=Laptop              # Filtrar por nombre o SKU de producto
&warehouse=W001              # Filtrar por ID de bodega
&type=IN                     # Filtrar por tipo: IN, OUT, ADJUST
```

Ejemplo completo:
```
http://localhost:8000/stock-moves?page=1&pageSize=5&product=Laptop&type=IN
```

## Estructura de Respuestas

### Login Exitoso
```json
{
  "id": "1234567890",
  "name": "Admin",
  "lastName": "User",
  "email": "admin@example.com",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Lista de Movimientos
```json
{
  "data": [
    {
      "id": "SM001",
      "date": "2026-01-15",
      "product": {
        "id": "P001",
        "name": "Laptop Dell XPS 13",
        "sku": "DELL-XPS13"
      },
      "warehouse": {
        "id": "W001",
        "name": "Bodega Central"
      },
      "type": "IN",
      "quantity": 50,
      "reference": "Compra inicial de laptops"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "pageSize": 10,
    "totalItems": 10,
    "totalPages": 1
  }
}
```

## Ejecutar Tests

```powershell
# Todos los tests
pytest -v

# Solo tests unitarios
pytest -m unit -v

# Solo tests E2E
pytest -m e2e -v

# Con reporte de cobertura
pytest --cov=app tests/
```

## Ejecutar con Docker (Opcional)

Si prefieres usar Docker:

```powershell
# Construir y ejecutar
docker-compose up --build

# Solo ejecutar (si ya está construido)
docker-compose up

# Detener
docker-compose down
```

## Troubleshooting

### Error: "No module named 'fastapi'"
Solución: Asegúrate de tener el entorno virtual activado y las dependencias instaladas:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Address already in use"
Solución: El puerto 8000 está ocupado. Usa otro puerto:
```powershell
uvicorn app.main:app --reload --port 8001
```

### Error: Token inválido
Solución: El token puede haber expirado (duración: 30 min). Haz login nuevamente.

### Error: Database locked
Solución: Cierra cualquier otra instancia de la aplicación que esté usando la DB.

## Comandos Útiles

```powershell
# Ver todas las tablas de la base de datos
python -c "from app.infrastructure.driven_adapter.persistence.config.database import Database, Base; from app.application.settings import settings; db = Database(settings.database_url); print([table for table in Base.metadata.tables.keys()])"

# Eliminar base de datos y empezar de nuevo
Remove-Item stock_api.db
python seed_data.py

# Ver logs en tiempo real
uvicorn app.main:app --reload --log-level debug
```

## Próximos Pasos

1. ✅ Explora la documentación Swagger: http://localhost:8000/api/docs
2. ✅ Prueba todos los endpoints
3. ✅ Revisa el código en las diferentes capas
4. ✅ Ejecuta los tests
5. ✅ Personaliza según tus necesidades

## Arquitectura del Proyecto

```
┌─────────────────────────────────────┐
│      Entry Points (Controllers)     │  ← FastAPI Routes
├─────────────────────────────────────┤
│        Use Cases (Business Logic)   │  ← Lógica de Negocio
├─────────────────────────────────────┤
│         Domain Models & Gateways    │  ← Modelos y Interfaces
├─────────────────────────────────────┤
│  Repositories & Database (SQLAlchemy)│ ← Persistencia
└─────────────────────────────────────┘
```

## Soporte

Si tienes problemas:
1. Revisa los logs de la aplicación
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el puerto 8000 esté disponible
4. Consulta el [README.md](README.md) para más detalles

---

¡Listo! Tu API REST con FastAPI está funcionando 🎉
