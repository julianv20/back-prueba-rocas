from fastapi import APIRouter, HTTPException

from app.application.container import Container
from app.infrastructure.entry_point.dto.user_dto import (
    LoginRequest, RegisterRequest, UserResponse
)
from app.infrastructure.entry_point.mapper.user_mapper import UserDTOMapper
from app.application.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()
container = Container()


@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest):
    logger.info(f"Login request for: {request.email}")
    
    auth_use_case = container.auth_use_case()
    user = await auth_use_case.login(request.email, request.password)
    
    return UserDTOMapper.to_response(user)


@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest):
    logger.info(f"Register request for: {request.email}")
    
    auth_use_case = container.auth_use_case()
    user = await auth_use_case.register(
        user_id=request.id,
        name=request.name,
        last_name=request.lastName,
        email=request.email,
        password=request.password
    )
    
    return UserDTOMapper.to_response(user)
