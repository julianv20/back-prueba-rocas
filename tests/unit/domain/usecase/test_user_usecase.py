"""Unit tests for UserUseCase"""
import pytest

from app.domain.usecase.user_usecase import UserUseCase
from app.domain.model.user import User
from app.domain.model.util.exceptions import UserNotFoundException
from app.infrastructure.driven_adapter.user_adapter.user_data_gateway_impl import (
    UserDataGatewayImpl
)


@pytest.mark.unit
class TestUserUseCase:
    """Test cases for UserUseCase"""
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_repository, sample_user):
        """Test getting user by ID successfully"""
        # Arrange
        created_user = await user_repository.create(sample_user)
        gateway = UserDataGatewayImpl(user_repository)
        use_case = UserUseCase(gateway)
        
        # Act
        result = await use_case.get_user_by_id(created_user.id)
        
        # Assert
        assert result.id == created_user.id
        assert result.email == created_user.email
        assert result.name == created_user.name
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, user_repository):
        """Test getting user by ID when user doesn't exist"""
        # Arrange
        gateway = UserDataGatewayImpl(user_repository)
        use_case = UserUseCase(gateway)
        
        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await use_case.get_user_by_id("nonexistent")
    
    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, user_repository, sample_user):
        """Test getting user by email successfully"""
        # Arrange
        created_user = await user_repository.create(sample_user)
        gateway = UserDataGatewayImpl(user_repository)
        use_case = UserUseCase(gateway)
        
        # Act
        result = await use_case.get_user_by_email(created_user.email)
        
        # Assert
        assert result.email == created_user.email
        assert result.name == created_user.name
