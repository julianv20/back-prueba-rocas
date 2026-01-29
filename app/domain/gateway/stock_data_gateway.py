"""Stock data gateway interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.model.stock import StockMove, Product, Warehouse
from app.domain.model.pagination import PaginatedResponse


class StockDataGateway(ABC):
    
    @abstractmethod
    async def find_stock_move_by_id(self, stock_move_id: str) -> Optional[StockMove]:
        pass
    
    @abstractmethod
    async def find_all_stock_moves(
        self,
        page: int,
        page_size: int,
        product_filter: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        move_type: Optional[str] = None,
    ) -> PaginatedResponse[StockMove]:
        pass
    
    @abstractmethod
    async def update_stock_move(self, stock_move: StockMove) -> StockMove:
        pass
    
    @abstractmethod
    async def create_stock_move(self, stock_move: StockMove) -> StockMove:
        pass
    
    @abstractmethod
    async def find_product_by_id(self, product_id: str) -> Optional[Product]:
        pass
    
    @abstractmethod
    async def find_all_products(self) -> List[Product]:
        pass
    
    @abstractmethod
    async def find_warehouse_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        pass
    
    @abstractmethod
    async def find_all_warehouses(self) -> List[Warehouse]:
        pass
