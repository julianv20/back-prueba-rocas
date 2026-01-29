"""Custom exceptions for the domain layer"""


class DomainException(Exception):
    
    def __init__(self, message: str = "Domain error occurred"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(DomainException):
    
    def __init__(self, user_id: str):
        super().__init__(f"User with ID {user_id} not found")


class UserAlreadyExistsException(DomainException):
    
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")


class InvalidCredentialsException(DomainException):
    
    def __init__(self):
        super().__init__("Invalid credentials provided")


class StockMoveNotFoundException(DomainException):
    
    def __init__(self, stock_move_id: str):
        super().__init__(f"Stock move with ID {stock_move_id} not found")


class ProductNotFoundException(DomainException):
    
    def __init__(self, product_id: str):
        super().__init__(f"Product with ID {product_id} not found")


class WarehouseNotFoundException(DomainException):
    
    def __init__(self, warehouse_id: str):
        super().__init__(f"Warehouse with ID {warehouse_id} not found")


class InvalidReferenceException(DomainException):
    
    def __init__(self):
        super().__init__("Reference must be between 3 and 60 characters")


class UnauthorizedException(DomainException):
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message)
