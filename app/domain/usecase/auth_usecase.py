"""Authentication use case"""
from typing import Optional

from app.domain.gateway.user_data_gateway import UserDataGateway
from app.domain.model.user import User
from app.domain.model.util.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException
)
from app.domain.usecase.util.security import SecurityService
from app.domain.usecase.util.jwt import JWTService
from app.application.logging_config import get_logger

logger = get_logger(__name__)


class AuthUseCase:
    
    def __init__(self, user_gateway: UserDataGateway) -> None:
        self.user_gateway = user_gateway
        self.security_service = SecurityService()
        self.jwt_service = JWTService()
    
    async def login(self, email: str, password: str) -> User:
        logger.info(f"Login attempt for email: {email}")
        
        user = await self.user_gateway.find_by_email(email)
        
        if not user:
            logger.warning(f"User not found: {email}")
            raise InvalidCredentialsException()
        
        if not self.security_service.verify_password(password, user.password):
            logger.warning(f"Invalid password for user: {email}")
            raise InvalidCredentialsException()
        
        token = self.jwt_service.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        
        user.token = token
        logger.info(f"User logged in successfully: {email}")
        
        return user
    
    async def register(self, user_id: str, name: str, last_name: str, 
                      email: str, password: str) -> User:
        logger.info(f"Registration attempt for email: {email}")
        
        if await self.user_gateway.exists_by_email(email):
            logger.warning(f"User already exists: {email}")
            raise UserAlreadyExistsException(email)
        
        hashed_password = self.security_service.hash_password(password)
        
        user = User(
            id=user_id,
            name=name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        
        created_user = await self.user_gateway.create(user)
        logger.info(f"User registered successfully: {email}")
        
        return created_user
    
    async def validate_token(self, token: str) -> Optional[str]:
        return self.jwt_service.extract_user_id(token)
