from datetime import date as date_type
from app.domain.model.stock import StockMove, Product, Warehouse, StockMoveType
from app.infrastructure.driven_adapter.persistence.entity.stock_entity import (
    StockMoveEntity, ProductEntity, WarehouseEntity
)


class StockMapper:
    
    @staticmethod
    def product_to_domain(entity: ProductEntity) -> Product:
        return Product(
            id=entity.id,
            name=entity.name,
            sku=entity.sku
        )
    
    @staticmethod
    def product_to_entity(domain: Product) -> ProductEntity:
        return ProductEntity(
            id=domain.id,
            name=domain.name,
            sku=domain.sku
        )
    
    @staticmethod
    def warehouse_to_domain(entity: WarehouseEntity) -> Warehouse:
        return Warehouse(
            id=entity.id,
            name=entity.name
        )
    
    @staticmethod
    def warehouse_to_entity(domain: Warehouse) -> WarehouseEntity:
        return WarehouseEntity(
            id=domain.id,
            name=domain.name
        )
    
    @staticmethod
    def stock_move_to_domain(entity: StockMoveEntity) -> StockMove:
        return StockMove(
            id=entity.id,
            date=entity.date,
            product=StockMapper.product_to_domain(entity.product),
            warehouse=StockMapper.warehouse_to_domain(entity.warehouse),
            type=StockMoveType(entity.type),
            quantity=entity.quantity,
            reference=entity.reference
        )
    
    @staticmethod
    def stock_move_to_entity(domain: StockMove) -> StockMoveEntity:
        return StockMoveEntity(
            id=domain.id,
            date=domain.date,
            product_id=domain.product.id,
            warehouse_id=domain.warehouse.id,
            type=domain.type,
            quantity=domain.quantity,
            reference=domain.reference
        )
