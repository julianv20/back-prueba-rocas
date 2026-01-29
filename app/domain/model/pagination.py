"""Pagination model"""
from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class Pagination:
    
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    
    def to_dict(self) -> dict:
        return {
            "currentPage": self.current_page,
            "pageSize": self.page_size,
            "totalItems": self.total_items,
            "totalPages": self.total_pages,
        }


@dataclass
class PaginatedResponse(Generic[T]):
    
    data: List[T]
    pagination: Pagination
    
    def to_dict(self, item_converter=None) -> dict:
        if item_converter:
            data = [item_converter(item) for item in self.data]
        else:
            data = [item.to_dict() if hasattr(item, 'to_dict') else item for item in self.data]
        
        return {
            "data": data,
            "pagination": self.pagination.to_dict(),
        }
