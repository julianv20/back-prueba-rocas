from typing import Optional, Callable
from sqlalchemy.orm import Session

from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity
from app.infrastructure.driven_adapter.persistence.user_repository.user_mapper import UserMapper
from app.domain.model.user import User


class SQLAlchemyUserRepository:
    
    def __init__(self, session_factory: Callable[..., Session]) -> None:
        self.session_factory = session_factory
    
    async def find_by_email(self, email: str) -> Optional[User]:
        with self.session_factory() as session:
            entity = session.query(UserEntity).filter(UserEntity.email == email).first()
            return UserMapper.to_domain(entity) if entity else None
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        with self.session_factory() as session:
            entity = session.query(UserEntity).filter(UserEntity.id == user_id).first()
            return UserMapper.to_domain(entity) if entity else None
    
    async def create(self, user: User) -> User:
        with self.session_factory() as session:
            entity = UserMapper.to_entity(user)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return UserMapper.to_domain(entity)
    
    async def update(self, user: User) -> User:
        with self.session_factory() as session:
            entity = session.query(UserEntity).filter(UserEntity.id == user.id).first()
            if entity:
                entity.name = user.name
                entity.last_name = user.last_name
                entity.email = user.email
                entity.password = user.password
                session.commit()
                session.refresh(entity)
                return UserMapper.to_domain(entity)
            raise ValueError(f"User {user.id} not found")
    
    async def exists_by_email(self, email: str) -> bool:
        with self.session_factory() as session:
            return session.query(UserEntity).filter(UserEntity.email == email).first() is not None
