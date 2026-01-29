# Guía de Estilo - Stock API

## Principios Generales

### 1. Clean Architecture (Arquitectura Hexagonal)

El proyecto sigue los principios de Clean Architecture con las siguientes capas:

- **Domain**: Lógica de negocio pura, independiente de frameworks
- **Application**: Configuración y orquestación
- **Infrastructure**: Implementaciones concretas (DB, API, etc.)

### 2. Separación de Responsabilidades

Cada capa tiene responsabilidades claras:

```
Domain (Núcleo)
├── Models: Entidades de negocio
├── Gateways: Interfaces (puertos)
└── Use Cases: Lógica de negocio

Application (Configuración)
├── Settings: Configuración
├── Container: Inyección de dependencias
└── Handler: Orquestación de rutas

Infrastructure (Adaptadores)
├── Driven Adapters: Implementaciones de gateways
└── Entry Points: Controllers, DTOs, Handlers
```

## Convenciones de Código

### Python

- **Estilo**: PEP 8
- **Formatter**: Black (línea de 100 caracteres)
- **Linter**: Ruff
- **Type Hints**: Obligatorio en funciones públicas

```python
# ✅ Correcto
async def get_user_by_id(self, user_id: str) -> User:
    """Get user by ID"""
    user = await self.user_gateway.find_by_id(user_id)
    return user

# ❌ Incorrecto
async def get_user_by_id(self, user_id):
    user = await self.user_gateway.find_by_id(user_id)
    return user
```

### Naming Conventions

- **Clases**: PascalCase
- **Funciones/Métodos**: snake_case
- **Constantes**: UPPER_SNAKE_CASE
- **Variables privadas**: Prefijo `_`

```python
# Classes
class UserUseCase:
    pass

# Functions
async def create_user(user: User) -> User:
    pass

# Constants
MAX_PAGE_SIZE = 100

# Private
def _hash_password(password: str) -> str:
    pass
```

### Imports

Orden de imports:

1. Standard library
2. Third-party
3. Local application

```python
# Standard library
from typing import Optional
from datetime import date

# Third-party
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# Local
from app.domain.model.user import User
from app.domain.usecase.auth_usecase import AuthUseCase
```

## Estructura de Archivos

### Modelos de Dominio

```python
@dataclass
class User:
    """User domain entity"""
    
    id: str
    name: str
    email: str
    
    def __post_init__(self) -> None:
        """Validate user data"""
        self._validate()
    
    def _validate(self) -> None:
        """Private validation method"""
        if not self.email:
            raise ValueError("Email is required")
```

### Use Cases

```python
class UserUseCase:
    """User business logic"""
    
    def __init__(self, user_gateway: UserDataGateway) -> None:
        self.user_gateway = user_gateway
    
    async def get_user(self, user_id: str) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            User domain model
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = await self.user_gateway.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user
```

### Controllers

```python
router = APIRouter()

@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest):
    """
    Login endpoint
    
    Authenticates user and returns JWT token
    """
    # Implementation
    pass
```

## DTOs (Data Transfer Objects)

- Usar Pydantic para validación
- Separar request y response DTOs
- Usar alias para camelCase en API

```python
class UserResponse(BaseModel):
    """User response DTO"""
    id: str
    name: str
    last_name: str = Field(alias="lastName")
    
    class Config:
        populate_by_name = True
```

## Manejo de Errores

### Excepciones Personalizadas

```python
class DomainException(Exception):
    """Base domain exception"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(DomainException):
    """User not found exception"""
    
    def __init__(self, user_id: str):
        super().__init__(f"User {user_id} not found")
```

### Exception Handlers

```python
@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "UserNotFound",
            "message": exc.message
        }
    )
```

## Testing

### Estructura de Tests

```python
@pytest.mark.unit
class TestUserUseCase:
    """Unit tests for UserUseCase"""
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, user_repository):
        """Test getting user successfully"""
        # Arrange
        user = User(id="123", name="Test")
        
        # Act
        result = await use_case.get_user(user.id)
        
        # Assert
        assert result.id == user.id
```

### Markers

- `@pytest.mark.unit`: Tests unitarios
- `@pytest.mark.e2e`: Tests end-to-end
- `@pytest.mark.asyncio`: Tests asíncronos

## Documentación

### Docstrings

Usar formato Google:

```python
async def create_user(self, user: User) -> User:
    """
    Create a new user
    
    Args:
        user: User domain model to create
        
    Returns:
        Created user with generated ID
        
    Raises:
        UserAlreadyExistsException: If email already exists
        
    Example:
        >>> user = User(id="123", name="John")
        >>> created = await use_case.create_user(user)
    """
```

## Logging

```python
from app.application.logging_config import get_logger

logger = get_logger(__name__)

# Usar niveles apropiados
logger.debug("Debug information")
logger.info("User logged in: {email}")
logger.warning("Invalid attempt")
logger.error("Error occurred", exc_info=True)
```

## Inyección de Dependencias

Usar dependency-injector:

```python
class Container(containers.DeclarativeContainer):
    """DI Container"""
    
    # Singleton para servicios
    database = providers.Singleton(Database)
    
    # Factory para repositorios
    user_repository = providers.Factory(
        UserRepository,
        session=database.provided.session
    )
```

## Buenas Prácticas

### 1. Single Responsibility Principle
Cada clase/función hace una sola cosa

### 2. Dependency Inversion
Depender de abstracciones, no implementaciones

### 3. Validación
- Validar en el dominio
- Usar Pydantic en DTOs
- Fail fast

### 4. Async/Await
- Usar async para I/O
- No bloquear el event loop

### 5. Type Hints
- Siempre usar type hints
- Usar Optional[] para valores opcionales

### 6. Comentarios
- Código auto-explicativo
- Comentar el "por qué", no el "qué"

## Git Commits

Formato de commits:

```
<type>: <subject>

<body>
```

Types:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato de código
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

Ejemplo:
```
feat: add user authentication with JWT

- Implement login endpoint
- Add JWT token generation
- Add authentication middleware
```

## Code Review Checklist

- [ ] Tests pasan
- [ ] Código formateado (Black)
- [ ] Sin errores de linting (Ruff)
- [ ] Documentación actualizada
- [ ] Type hints presentes
- [ ] Separación de responsabilidades clara
- [ ] Manejo de errores apropiado
- [ ] Logs informativos
