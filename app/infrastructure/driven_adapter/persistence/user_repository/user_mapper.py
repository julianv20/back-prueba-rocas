from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity


class UserMapper:
    
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        return User(
            id=entity.id,
            name=entity.name,
            last_name=entity.last_name,
            email=entity.email,
            password=entity.password
        )
    
    @staticmethod
    def to_entity(domain: User) -> UserEntity:
        return UserEntity(
            id=domain.id,
            name=domain.name,
            last_name=domain.last_name,
            email=domain.email,
            password=domain.password
        )
