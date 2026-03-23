import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.db import Base


# ✅ In-memory SQLite DB
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ✅ Setup fresh DB per test
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# ✅ Override SessionLocal used in routes
@pytest.fixture(scope="function")
def test_client(db_session, monkeypatch):
    app = create_app()

    # 🔥 override SessionLocal to always return test DB session
    def override_session():
        return db_session

    monkeypatch.setattr("app.routes.SessionLocal", override_session)

    with app.test_client() as client:
        yield client