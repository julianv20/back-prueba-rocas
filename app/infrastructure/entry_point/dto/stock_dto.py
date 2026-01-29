from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from enum import Enum


class StockMoveTypeDTO(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


class ProductDTO(BaseModel):
    id: str
    name: str
    sku: Optional[str] = None


class WarehouseDTO(BaseModel):
    id: str
    name: str


class StockMoveDTO(BaseModel):
    id: str
    date: str
    product: ProductDTO
    warehouse: WarehouseDTO
    type: StockMoveTypeDTO
    quantity: int
    reference: str


class UpdateReferenceRequest(BaseModel):
    reference: str = Field(..., min_length=3, max_length=60)


class PaginationDTO(BaseModel):
    currentPage: int
    pageSize: int
    totalItems: int
    totalPages: int


class StockMovesListResponse(BaseModel):
    data: list[StockMoveDTO]
    pagination: PaginationDTO


class ProductsListResponse(BaseModel):
    data: list[ProductDTO]


class WarehousesListResponse(BaseModel):
    data: list[WarehouseDTO]
