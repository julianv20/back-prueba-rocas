from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Any] = None
