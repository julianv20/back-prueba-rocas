"""Stock use case"""
from typing import Optional, List

from app.domain.gateway.stock_data_gateway import StockDataGateway
from app.domain.model.stock import StockMove, Product, Warehouse
from app.domain.model.pagination import PaginatedResponse
from app.domain.model.util.exceptions import (
    StockMoveNotFoundException,
    InvalidReferenceException
)
from app.application.logging_config import get_logger

logger = get_logger(__name__)


class StockUseCase:
    
    def __init__(self, stock_gateway: StockDataGateway) -> None:
        self.stock_gateway = stock_gateway
    
    async def get_stock_moves(
        self,
        page: int = 1,
        page_size: int = 10,
        product_filter: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        move_type: Optional[str] = None,
    ) -> PaginatedResponse[StockMove]:
        logger.info(f"Fetching stock moves - page: {page}, size: {page_size}")
        
        return await self.stock_gateway.find_all_stock_moves(
            page=page,
            page_size=page_size,
            product_filter=product_filter,
            warehouse_id=warehouse_id,
            move_type=move_type
        )
    
    async def get_stock_move_by_id(self, stock_move_id: str) -> StockMove:
        stock_move = await self.stock_gateway.find_stock_move_by_id(stock_move_id)
        
        if not stock_move:
            logger.warning(f"Stock move not found: {stock_move_id}")
            raise StockMoveNotFoundException(stock_move_id)
        
        return stock_move
    
    async def update_stock_move_reference(
        self, stock_move_id: str, new_reference: str
    ) -> StockMove:
        logger.info(f"Updating reference for stock move: {stock_move_id}")
        
        stock_move = await self.get_stock_move_by_id(stock_move_id)
        
        try:
            stock_move.update_reference(new_reference)
        except ValueError:
            raise InvalidReferenceException()
        
        updated = await self.stock_gateway.update_stock_move(stock_move)
        logger.info(f"Stock move reference updated: {stock_move_id}")
        
        return updated
    
    async def get_all_products(self) -> List[Product]:
        logger.info("Fetching all products")
        return await self.stock_gateway.find_all_products()
    
    async def get_all_warehouses(self) -> List[Warehouse]:
        logger.info("Fetching all warehouses")
        return await self.stock_gateway.find_all_warehouses()
