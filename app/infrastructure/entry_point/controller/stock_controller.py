from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.application.container import Container
from app.infrastructure.entry_point.dto.stock_dto import (
    StockMoveDTO, UpdateReferenceRequest, StockMovesListResponse,
    ProductsListResponse, WarehousesListResponse
)
from app.infrastructure.entry_point.mapper.stock_mapper import StockDTOMapper
from app.infrastructure.entry_point.handler.auth_handler import get_current_user_id
from app.application.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()
container = Container()


@router.get("/products", response_model=ProductsListResponse, tags=["Products"])
async def get_all_products(
    current_user_id: str = Depends(get_current_user_id)
):
    logger.info(f"Get all products - User: {current_user_id}")
    
    stock_use_case = container.stock_use_case()
    products = await stock_use_case.get_all_products()
    
    return StockDTOMapper.products_to_list_response(products)


@router.get("/warehouses", response_model=WarehousesListResponse, tags=["Warehouses"])
async def get_all_warehouses(
    current_user_id: str = Depends(get_current_user_id)
):
    logger.info(f"Get all warehouses - User: {current_user_id}")
    
    stock_use_case = container.stock_use_case()
    warehouses = await stock_use_case.get_all_warehouses()
    
    return StockDTOMapper.warehouses_to_list_response(warehouses)


@router.get("", response_model=StockMovesListResponse)
async def get_stock_moves(
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(10, ge=1, le=100, description="Items per page", alias="pageSize"),
    product: Optional[str] = Query(None, description="Filter by product name or SKU"),
    warehouse: Optional[str] = Query(None, description="Filter by warehouse ID"),
    type: Optional[str] = Query(None, description="Filter by type (IN, OUT, ADJUST)"),
    current_user_id: str = Depends(get_current_user_id)
):
    logger.info(f"Get stock moves - User: {current_user_id}, Page: {page}")
    
    stock_use_case = container.stock_use_case()
    paginated = await stock_use_case.get_stock_moves(
        page=page,
        page_size=pageSize,
        product_filter=product,
        warehouse_id=warehouse,
        move_type=type
    )
    
    return StockDTOMapper.paginated_to_list_response(paginated)


@router.get("/{stock_move_id}", response_model=StockMoveDTO)
async def get_stock_move_by_id(
    stock_move_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    logger.info(f"Get stock move: {stock_move_id} - User: {current_user_id}")
    
    stock_use_case = container.stock_use_case()
    stock_move = await stock_use_case.get_stock_move_by_id(stock_move_id)
    
    return StockDTOMapper.stock_move_to_dto(stock_move)


@router.patch("/{stock_move_id}", response_model=StockMoveDTO)
async def update_stock_move_reference(
    stock_move_id: str,
    request: UpdateReferenceRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    logger.info(f"Update stock move reference: {stock_move_id} - User: {current_user_id}")
    
    stock_use_case = container.stock_use_case()
    updated = await stock_use_case.update_stock_move_reference(
        stock_move_id=stock_move_id,
        new_reference=request.reference
    )
    
    return StockDTOMapper.stock_move_to_dto(updated)