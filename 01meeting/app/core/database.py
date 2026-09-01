from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
from .config import settings
from app.models import Base

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """Get the database URL, handling SQLite path creation."""
    url = settings.database_url
    if url.startswith("sqlite"):
        import os
        db_path = url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    return url


def create_db_engine() -> Engine:
    """Create and return a database engine."""
    url = get_database_url()
    logger.info(f"Creating database engine with URL: {url}")

    if "sqlite" in url:
        engine = create_engine(
            url,
            echo=settings.database_echo,
            connect_args={"check_same_thread": False},
        )
    else:
        engine = create_engine(
            url,
            echo=settings.database_echo,
            pool_pre_ping=True,
        )

    return engine


def init_db() -> None:
    """Initialize the database by creating all tables."""
    engine = create_db_engine()
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


# Create engine and session factory
engine = create_db_engine()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Dependency injection for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
