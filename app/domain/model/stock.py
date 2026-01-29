"""Stock domain models"""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class StockMoveType(str, Enum):
    
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


@dataclass
class Product:
    
    id: str
    name: str
    sku: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
        }


@dataclass
class Warehouse:
    
    id: str
    name: str
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }


@dataclass
class StockMove:
    
    id: str
    date: date
    product: Product
    warehouse: Warehouse
    type: StockMoveType
    quantity: int
    reference: str
    
    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.validate_reference()
    
    def validate_reference(self) -> None:
        if not self.reference or len(self.reference) < 3 or len(self.reference) > 60:
            from app.domain.model.util.exceptions import InvalidReferenceException
            raise InvalidReferenceException()
    
    def update_reference(self, new_reference: str) -> None:
        self.reference = new_reference
        self.validate_reference()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "product": self.product.to_dict(),
            "warehouse": self.warehouse.to_dict(),
            "type": self.type.value,
            "quantity": self.quantity,
            "reference": self.reference,
        }
