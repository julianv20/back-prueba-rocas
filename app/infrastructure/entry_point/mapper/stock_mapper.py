from app.domain.model.stock import StockMove, Product, Warehouse
from app.domain.model.pagination import PaginatedResponse
from app.infrastructure.entry_point.dto.stock_dto import (
    StockMoveDTO, ProductDTO, WarehouseDTO, StockMovesListResponse, PaginationDTO,
    ProductsListResponse, WarehousesListResponse
)


class StockDTOMapper:
    
    @staticmethod
    def product_to_dto(product: Product) -> ProductDTO:
        return ProductDTO(
            id=product.id,
            name=product.name,
            sku=product.sku
        )
    
    @staticmethod
    def warehouse_to_dto(warehouse: Warehouse) -> WarehouseDTO:
        return WarehouseDTO(
            id=warehouse.id,
            name=warehouse.name
        )
    
    @staticmethod
    def stock_move_to_dto(stock_move: StockMove) -> StockMoveDTO:
        return StockMoveDTO(
            id=stock_move.id,
            date=stock_move.date.isoformat(),
            product=StockDTOMapper.product_to_dto(stock_move.product),
            warehouse=StockDTOMapper.warehouse_to_dto(stock_move.warehouse),
            type=stock_move.type,
            quantity=stock_move.quantity,
            reference=stock_move.reference
        )
    
    @staticmethod
    def paginated_to_list_response(
        paginated: PaginatedResponse[StockMove]
    ) -> StockMovesListResponse:
        return StockMovesListResponse(
            data=[StockDTOMapper.stock_move_to_dto(sm) for sm in paginated.data],
            pagination=PaginationDTO(
                currentPage=paginated.pagination.current_page,
                pageSize=paginated.pagination.page_size,
                totalItems=paginated.pagination.total_items,
                totalPages=paginated.pagination.total_pages
            )
        )
    
    @staticmethod
    def products_to_list_response(products: list[Product]) -> ProductsListResponse:
        return ProductsListResponse(
            data=[StockDTOMapper.product_to_dto(p) for p in products]
        )
    
    @staticmethod
    def warehouses_to_list_response(warehouses: list[Warehouse]) -> WarehousesListResponse:
        return WarehousesListResponse(
            data=[StockDTOMapper.warehouse_to_dto(w) for w in warehouses]
        )
