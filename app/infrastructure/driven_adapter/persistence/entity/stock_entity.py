from sqlalchemy import Column, String, Integer, Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.driven_adapter.persistence.config.database import Base
from app.domain.model.stock import StockMoveType


class ProductEntity(Base):
    
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=True)
    
    stock_moves = relationship("StockMoveEntity", back_populates="product")
    
    def __repr__(self) -> str:
        return f"<ProductEntity(id={self.id}, name={self.name})>"


class WarehouseEntity(Base):
    
    __tablename__ = "warehouses"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    stock_moves = relationship("StockMoveEntity", back_populates="warehouse")
    
    def __repr__(self) -> str:
        return f"<WarehouseEntity(id={self.id}, name={self.name})>"


class StockMoveEntity(Base):
    
    __tablename__ = "stock_moves"
    
    id = Column(String, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    type = Column(SQLEnum(StockMoveType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference = Column(String, nullable=False)
    
    product = relationship("ProductEntity", back_populates="stock_moves")
    warehouse = relationship("WarehouseEntity", back_populates="stock_moves")
    
    def __repr__(self) -> str:
        return f"<StockMoveEntity(id={self.id}, type={self.type}, quantity={self.quantity})>"
