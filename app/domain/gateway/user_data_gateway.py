"""User data gateway interface"""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.model.user import User


class UserDataGateway(ABC):
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass
