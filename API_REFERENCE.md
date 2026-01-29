# 📋 Referencia Rápida de API - Stock API

## 🎯 Estado del Servidor

✅ **Servidor ejecutándose**: http://localhost:8000
✅ **Documentación Swagger**: http://localhost:8000/api/docs
✅ **Base de datos poblada** con datos de prueba

## 👤 Credenciales de Prueba

### Usuario Admin
```
Email: admin@example.com
Password: admin123
```

### Usuario Test
```
Email: test@example.com
Password: test123
```

## 🔐 Flujo de Autenticación

### 1. Login (Obtener Token)

```http
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "id": "1234567890",
  "name": "Admin",
  "lastName": "User",
  "email": "admin@example.com",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**⚠️ IMPORTANTE:** Guarda el `token` de la respuesta. Lo necesitarás para todos los demás endpoints.

### 2. Registrar Nuevo Usuario (Opcional)

```http
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "id": "9876543210",
  "name": "Juan",
  "lastName": "Pérez",
  "email": "juan@example.com",
  "password": "password123"
}
```

## 📦 Endpoints de Stock Moves

**Todos requieren el header de autenticación:**
```
Authorization: Bearer <tu_token_aqui>
```

### 3. Listar Movimientos (con Filtros y Paginación)

```http
GET http://localhost:8000/stock-moves?page=1&pageSize=10
Authorization: Bearer <token>
```

**Parámetros opcionales:**
- `page` - Número de página (default: 1)
- `pageSize` - Items por página (default: 10, max: 100)
- `product` - Filtrar por nombre o SKU de producto
- `warehouse` - Filtrar por ID de bodega (W001, W002, W003)
- `type` - Filtrar por tipo (IN, OUT, ADJUST)

**Ejemplos de filtros:**

```http
# Solo productos con "Laptop" en el nombre
GET http://localhost:8000/stock-moves?product=Laptop

# Solo movimientos de la Bodega Central
GET http://localhost:8000/stock-moves?warehouse=W001

# Solo movimientos de entrada (IN)
GET http://localhost:8000/stock-moves?type=IN

# Combinación de filtros
GET http://localhost:8000/stock-moves?type=IN&warehouse=W001&page=1&pageSize=5
```

**Respuesta:**
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

### 4. Obtener Movimiento por ID

```http
GET http://localhost:8000/stock-moves/SM001
Authorization: Bearer <token>
```

**Respuesta:**
```json
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
```

### 5. Actualizar Referencia de Movimiento

```http
PATCH http://localhost:8000/stock-moves/SM001
Authorization: Bearer <token>
Content-Type: application/json

{
  "reference": "Nueva referencia actualizada - Compra Q1 2026"
}
```

**Validación:**
- La referencia debe tener entre **3 y 60 caracteres**

**Respuesta:**
```json
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
  "reference": "Nueva referencia actualizada - Compra Q1 2026"
}
```

## 📊 Datos de Prueba Disponibles

### Productos
- `P001` - Laptop Dell XPS 13 (SKU: DELL-XPS13)
- `P002` - iPhone 15 Pro (SKU: IPHONE-15P)
- `P003` - Samsung Galaxy S24 (SKU: SAM-S24)
- `P004` - MacBook Pro M3 (SKU: MBP-M3)
- `P005` - iPad Air (SKU: IPAD-AIR)

### Bodegas
- `W001` - Bodega Central
- `W002` - Bodega Norte
- `W003` - Bodega Sur

### Stock Moves
- `SM001` a `SM010` - 10 movimientos de prueba

### Tipos de Movimiento
- `IN` - Entrada de inventario
- `OUT` - Salida de inventario
- `ADJUST` - Ajuste de inventario

## 🧪 Probar con cURL (PowerShell)

### Login
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email":"admin@example.com","password":"admin123"}'

$token = $response.token
Write-Host "Token: $token"
```

### Listar Movimientos
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/stock-moves?page=1&pageSize=10" `
  -Headers @{"Authorization"="Bearer $token"}
```

### Actualizar Referencia
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/stock-moves/SM001" `
  -Method PATCH `
  -Headers @{"Authorization"="Bearer $token"} `
  -ContentType "application/json" `
  -Body '{"reference":"Nueva referencia desde PowerShell"}'
```

## 🔍 Probar con Postman

1. **Crear nueva colección**: "Stock API"

2. **Configurar variables de colección:**
   - `baseUrl`: `http://localhost:8000`
   - `token`: (se llenará después del login)

3. **Request de Login:**
   - Method: POST
   - URL: `{{baseUrl}}/auth/login`
   - Body (JSON):
     ```json
     {
       "email": "admin@example.com",
       "password": "admin123"
     }
     ```
   - En "Tests", agregar:
     ```javascript
     pm.collectionVariables.set("token", pm.response.json().token);
     ```

4. **Request de Stock Moves:**
   - Method: GET
   - URL: `{{baseUrl}}/stock-moves`
   - Headers:
     - `Authorization`: `Bearer {{token}}`

## ⚠️ Códigos de Error Comunes

| Código | Error | Descripción |
|--------|-------|-------------|
| 401 | Unauthorized | Token inválido o expirado |
| 404 | Not Found | Recurso no encontrado |
| 400 | Bad Request | Datos inválidos |
| 409 | Conflict | Usuario ya existe |
| 500 | Internal Server Error | Error del servidor |

**Ejemplo de respuesta de error:**
```json
{
  "success": false,
  "error": "InvalidCredentials",
  "message": "Invalid credentials provided"
}
```

## 🎨 Probar con Swagger UI (Recomendado)

**URL:** http://localhost:8000/api/docs

1. Abre Swagger en tu navegador
2. Click en "POST /auth/login"
3. Click en "Try it out"
4. Ingresa las credenciales
5. Click en "Execute"
6. **Copia el token** de la respuesta
7. Click en el botón "Authorize" (candado verde arriba a la derecha)
8. Ingresa: `Bearer <tu_token>`
9. Ahora puedes probar todos los demás endpoints

## 📝 Notas Importantes

1. **Token Expiration:** Los tokens expiran en **30 minutos**
2. **Page Size Limit:** El tamaño máximo de página es **100**
3. **Reference Length:** La referencia debe tener entre **3 y 60 caracteres**
4. **CORS:** Configurado para localhost:3000 y localhost:5173

## 🚀 Comandos Útiles

```powershell
# Iniciar servidor
C:/Users/yefer/OneDrive/Desktop/stock-api/venv/Scripts/python.exe -m uvicorn app.main:app --reload

# Poblar base de datos nuevamente
C:/Users/yefer/OneDrive/Desktop/stock-api/venv/Scripts/python.exe seed_data.py

# Ejecutar tests
C:/Users/yefer/OneDrive/Desktop/stock-api/venv/Scripts/python.exe -m pytest -v
```

## 🎯 Flujo Completo de Ejemplo

```http
# 1. Login
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}

# Respuesta: { ..., "token": "abc123..." }

# 2. Listar todos los movimientos
GET http://localhost:8000/stock-moves?page=1&pageSize=10
Authorization: Bearer abc123...

# 3. Filtrar solo productos "Laptop"
GET http://localhost:8000/stock-moves?product=Laptop
Authorization: Bearer abc123...

# 4. Obtener detalles de SM001
GET http://localhost:8000/stock-moves/SM001
Authorization: Bearer abc123...

# 5. Actualizar referencia de SM001
PATCH http://localhost:8000/stock-moves/SM001
Authorization: Bearer abc123...
Content-Type: application/json

{
  "reference": "Referencia actualizada correctamente"
}
```

---

**✅ API funcionando correctamente!**
**📚 Documentación interactiva:** http://localhost:8000/api/docs
