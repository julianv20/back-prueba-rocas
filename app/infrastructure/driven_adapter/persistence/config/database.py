from typing import Callable
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.application.logging_config import get_logger

logger = get_logger(__name__)

Base = declarative_base()


class Database:
    
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
            echo=False
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        logger.info(f"Database initialized: {database_url}")
    
    def create_database(self) -> None:
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created")
    
    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Session:
        return self._session_factory()
