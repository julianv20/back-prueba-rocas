"""Application handler - Wire up routes and dependencies"""
from fastapi import FastAPI

from app.application.container import Container
from app.infrastructure.entry_point.controller.auth_controller import router as auth_router
from app.infrastructure.entry_point.controller.stock_controller import router as stock_router


def setup_routes(app: FastAPI, container: Container) -> None:
    
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(stock_router, prefix="/stock-moves", tags=["Stock Moves"])
    
    @app.get("/", tags=["Health"])
    async def health_check():
        return {
            "status": "ok",
            "message": "Stock API is running"
        }
    
    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "healthy",
            "service": "stock-api",
            "version": "1.0.0"
        }
