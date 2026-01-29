from typing import Optional, List

from app.domain.gateway.stock_data_gateway import StockDataGateway
from app.domain.model.stock import StockMove, Product, Warehouse
from app.domain.model.pagination import PaginatedResponse
from app.infrastructure.driven_adapter.persistence.stock_repository.sqlalchemy_stock_repository import (
    SQLAlchemyStockRepository
)


class StockDataGatewayImpl(StockDataGateway):
    
    def __init__(self, stock_repository: SQLAlchemyStockRepository) -> None:
        self.stock_repository = stock_repository
    
    async def find_stock_move_by_id(self, stock_move_id: str) -> Optional[StockMove]:
        return await self.stock_repository.find_stock_move_by_id(stock_move_id)
    
    async def find_all_stock_moves(
        self,
        page: int,
        page_size: int,
        product_filter: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        move_type: Optional[str] = None,
    ) -> PaginatedResponse[StockMove]:
        return await self.stock_repository.find_all_stock_moves(
            page=page,
            page_size=page_size,
            product_filter=product_filter,
            warehouse_id=warehouse_id,
            move_type=move_type
        )
    
    async def update_stock_move(self, stock_move: StockMove) -> StockMove:
        return await self.stock_repository.update_stock_move(stock_move)
    
    async def create_stock_move(self, stock_move: StockMove) -> StockMove:
        return await self.stock_repository.create_stock_move(stock_move)
    
    async def find_product_by_id(self, product_id: str) -> Optional[Product]:
        return await self.stock_repository.find_product_by_id(product_id)
    
    async def find_all_products(self) -> List[Product]:
        return await self.stock_repository.find_all_products()
    
    async def find_warehouse_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        return await self.stock_repository.find_warehouse_by_id(warehouse_id)
    
    async def find_all_warehouses(self) -> List[Warehouse]:
        return await self.stock_repository.find_all_warehouses()
