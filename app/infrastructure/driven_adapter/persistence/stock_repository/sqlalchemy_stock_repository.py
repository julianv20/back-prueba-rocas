from typing import Optional, List, Callable
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from math import ceil

from app.infrastructure.driven_adapter.persistence.entity.stock_entity import (
    StockMoveEntity, ProductEntity, WarehouseEntity
)
from app.infrastructure.driven_adapter.persistence.stock_repository.stock_mapper import StockMapper
from app.domain.model.stock import StockMove, Product, Warehouse
from app.domain.model.pagination import PaginatedResponse, Pagination


class SQLAlchemyStockRepository:
    
    def __init__(self, session_factory: Callable[..., Session]) -> None:
        self.session_factory = session_factory
    
    async def find_stock_move_by_id(self, stock_move_id: str) -> Optional[StockMove]:
        with self.session_factory() as session:
            entity = session.query(StockMoveEntity).filter(
                StockMoveEntity.id == stock_move_id
            ).first()
            return StockMapper.stock_move_to_domain(entity) if entity else None
    
    async def find_all_stock_moves(
        self,
        page: int,
        page_size: int,
        product_filter: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        move_type: Optional[str] = None,
    ) -> PaginatedResponse[StockMove]:
        with self.session_factory() as session:
            query = session.query(StockMoveEntity)
            
            if product_filter:
                query = query.join(ProductEntity).filter(
                    or_(
                        ProductEntity.name.ilike(f"%{product_filter}%"),
                        ProductEntity.sku.ilike(f"%{product_filter}%")
                    )
                )
            
            if warehouse_id:
                query = query.filter(StockMoveEntity.warehouse_id == warehouse_id)
            
            if move_type:
                query = query.filter(StockMoveEntity.type == move_type)
            
            total_items = query.count()
            
            offset = (page - 1) * page_size
            entities = query.order_by(StockMoveEntity.date.desc()).offset(offset).limit(page_size).all()
            
            stock_moves = [StockMapper.stock_move_to_domain(entity) for entity in entities]
            
            total_pages = ceil(total_items / page_size) if page_size > 0 else 0
            pagination = Pagination(
                current_page=page,
                page_size=page_size,
                total_items=total_items,
                total_pages=total_pages
            )
            
            return PaginatedResponse(data=stock_moves, pagination=pagination)
    
    async def update_stock_move(self, stock_move: StockMove) -> StockMove:
        with self.session_factory() as session:
            entity = session.query(StockMoveEntity).filter(
                StockMoveEntity.id == stock_move.id
            ).first()
            
            if entity:
                entity.reference = stock_move.reference
                entity.date = stock_move.date
                entity.quantity = stock_move.quantity
                entity.type = stock_move.type
                session.commit()
                session.refresh(entity)
                return StockMapper.stock_move_to_domain(entity)
            
            raise ValueError(f"Stock move {stock_move.id} not found")
    
    async def create_stock_move(self, stock_move: StockMove) -> StockMove:
        with self.session_factory() as session:
            entity = StockMapper.stock_move_to_entity(stock_move)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return StockMapper.stock_move_to_domain(entity)
    
    async def find_product_by_id(self, product_id: str) -> Optional[Product]:
        with self.session_factory() as session:
            entity = session.query(ProductEntity).filter(ProductEntity.id == product_id).first()
            return StockMapper.product_to_domain(entity) if entity else None
    
    async def find_all_products(self) -> List[Product]:
        with self.session_factory() as session:
            entities = session.query(ProductEntity).all()
            return [StockMapper.product_to_domain(entity) for entity in entities]
    
    async def find_warehouse_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        with self.session_factory() as session:
            entity = session.query(WarehouseEntity).filter(WarehouseEntity.id == warehouse_id).first()
            return StockMapper.warehouse_to_domain(entity) if entity else None
    
    async def find_all_warehouses(self) -> List[Warehouse]:
        with self.session_factory() as session:
            entities = session.query(WarehouseEntity).all()
            return [StockMapper.warehouse_to_domain(entity) for entity in entities]
    
    async def create_product(self, product: Product) -> Product:
        with self.session_factory() as session:
            entity = StockMapper.product_to_entity(product)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return StockMapper.product_to_domain(entity)
    
    async def create_warehouse(self, warehouse: Warehouse) -> Warehouse:
        with self.session_factory() as session:
            entity = StockMapper.warehouse_to_entity(warehouse)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return StockMapper.warehouse_to_domain(entity)
