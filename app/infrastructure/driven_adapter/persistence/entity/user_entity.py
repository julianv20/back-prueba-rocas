from sqlalchemy import Column, String
from app.infrastructure.driven_adapter.persistence.config.database import Base


class UserEntity(Base):
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    def __repr__(self) -> str:
        return f"<UserEntity(id={self.id}, email={self.email})>"
