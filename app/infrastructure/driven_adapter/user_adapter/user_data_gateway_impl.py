from typing import Optional

from app.domain.gateway.user_data_gateway import UserDataGateway
from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)


class UserDataGatewayImpl(UserDataGateway):
    
    def __init__(self, user_repository: SQLAlchemyUserRepository) -> None:
        self.user_repository = user_repository
    
    async def find_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.find_by_email(email)
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        return await self.user_repository.find_by_id(user_id)
    
    async def create(self, user: User) -> User:
        return await self.user_repository.create(user)
    
    async def update(self, user: User) -> User:
        return await self.user_repository.update(user)
    
    async def exists_by_email(self, email: str) -> bool:
        return await self.user_repository.exists_by_email(email)
