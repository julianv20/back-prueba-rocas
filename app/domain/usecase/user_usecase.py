"""User use case"""
from typing import Optional

from app.domain.gateway.user_data_gateway import UserDataGateway
from app.domain.model.user import User
from app.domain.model.util.exceptions import UserNotFoundException
from app.application.logging_config import get_logger

logger = get_logger(__name__)


class UserUseCase:
    
    def __init__(self, user_gateway: UserDataGateway) -> None:
        self.user_gateway = user_gateway
    
    async def get_user_by_id(self, user_id: str) -> User:
        user = await self.user_gateway.find_by_id(user_id)
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserNotFoundException(user_id)
        
        return user
    
    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_gateway.find_by_email(email)
        
        if not user:
            logger.warning(f"User not found with email: {email}")
            raise UserNotFoundException(email)
        
        return user
