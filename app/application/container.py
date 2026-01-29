"""Dependency injection container"""
from dependency_injector import containers, providers

from app.application.settings import settings
from app.domain.usecase.auth_usecase import AuthUseCase
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.stock_usecase import StockUseCase
from app.infrastructure.driven_adapter.persistence.config.database import Database
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from app.infrastructure.driven_adapter.persistence.stock_repository.sqlalchemy_stock_repository import (
    SQLAlchemyStockRepository
)
from app.infrastructure.driven_adapter.user_adapter.user_data_gateway_impl import (
    UserDataGatewayImpl
)
from app.infrastructure.driven_adapter.stock_adapter.stock_data_gateway_impl import (
    StockDataGatewayImpl
)


class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    database = providers.Singleton(
        Database,
        database_url=settings.database_url
    )
    
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session_factory=database.provided.session
    )
    
    stock_repository = providers.Factory(
        SQLAlchemyStockRepository,
        session_factory=database.provided.session
    )
    
    user_gateway = providers.Factory(
        UserDataGatewayImpl,
        user_repository=user_repository
    )
    
    stock_gateway = providers.Factory(
        StockDataGatewayImpl,
        stock_repository=stock_repository
    )
    
    auth_use_case = providers.Factory(
        AuthUseCase,
        user_gateway=user_gateway
    )
    
    user_use_case = providers.Factory(
        UserUseCase,
        user_gateway=user_gateway
    )
    
    stock_use_case = providers.Factory(
        StockUseCase,
        stock_gateway=stock_gateway
    )
