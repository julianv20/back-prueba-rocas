from typing import Optional
from fastapi import Header, HTTPException

from app.application.container import Container
from app.domain.model.util.exceptions import UnauthorizedException
from app.application.logging_config import get_logger

logger = get_logger(__name__)

container = Container()


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        token = parts[1]
        
        auth_use_case = container.auth_use_case()
        user_id = await auth_use_case.validate_token(token)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return user_id
        
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
