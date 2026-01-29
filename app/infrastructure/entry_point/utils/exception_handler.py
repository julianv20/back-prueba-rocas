from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.model.util.exceptions import (
    DomainException,
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    StockMoveNotFoundException,
    InvalidReferenceException,
    UnauthorizedException
)
from app.application.logging_config import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    
    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        logger.warning(f"Invalid credentials: {exc.message}")
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": "InvalidCredentials",
                "message": exc.message
            }
        )
    
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        logger.warning(f"User not found: {exc.message}")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "UserNotFound",
                "message": exc.message
            }
        )
    
    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        logger.warning(f"User already exists: {exc.message}")
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error": "UserAlreadyExists",
                "message": exc.message
            }
        )
    
    @app.exception_handler(StockMoveNotFoundException)
    async def stock_move_not_found_handler(request: Request, exc: StockMoveNotFoundException):
        logger.warning(f"Stock move not found: {exc.message}")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "StockMoveNotFound",
                "message": exc.message
            }
        )
    
    @app.exception_handler(InvalidReferenceException)
    async def invalid_reference_handler(request: Request, exc: InvalidReferenceException):
        logger.warning(f"Invalid reference: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "InvalidReference",
                "message": exc.message
            }
        )
    
    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        logger.warning(f"Unauthorized: {exc.message}")
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "error": "Unauthorized",
                "message": exc.message
            }
        )
    
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        logger.error(f"Domain exception: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "DomainError",
                "message": exc.message
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "InternalServerError",
                "message": "An unexpected error occurred"
            }
        )
