from typing import TypeVar, Optional, Any
from fastapi.responses import JSONResponse

T = TypeVar("T")


class ApiResponseBuilder:
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> dict:
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(error: str, message: str, status_code: int = 400) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": error,
                "message": message
            }
        )
