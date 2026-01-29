"""Main application entry point"""
from app.application.fast_api import create_app
from app.application.handler import setup_routes
from app.application.container import Container
from app.infrastructure.driven_adapter.persistence.config.database import Database
from app.application.settings import settings
from app.application.logging_config import get_logger

logger = get_logger(__name__)

container = Container()

db = Database(database_url=settings.database_url)

db.create_database()
logger.info("Database initialized")

app = create_app()

setup_routes(app, container)

logger.info("Application started successfully")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
