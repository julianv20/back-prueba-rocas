"""Test configuration and fixtures"""
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.driven_adapter.persistence.config.database import Base
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from app.domain.model.user import User
from app.domain.usecase.util.security import SecurityService


@pytest.fixture(scope="function")
def test_db():
    """Create a test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield SessionLocal
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_repository(test_db):
    """Create user repository with test database"""
    return SQLAlchemyUserRepository(session_factory=test_db)


@pytest.fixture
def sample_user():
    """Create a sample user"""
    security = SecurityService()
    return User(
        id="1234567890",
        name="Test",
        last_name="User",
        email="test@example.com",
        password=security.hash_password("password123")
    )
