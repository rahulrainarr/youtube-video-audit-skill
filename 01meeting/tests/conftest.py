import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_db():
    """Create a test database."""
    from app.models import Base

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def temp_upload_dir(tmp_path):
    """Create a temporary upload directory for file tests."""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    return upload_dir


@pytest.fixture
def mock_settings():
    """Provide mock settings for testing."""
    from app.core import Settings

    return Settings(
        database_url="sqlite:///:memory:",
        transcription_provider="faster_whisper",
        llm_provider="claude",
        max_upload_size_mb=5000,
        temp_dir=":memory:",
        debug=True,
    )
