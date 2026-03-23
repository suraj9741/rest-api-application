import pytest
from app import create_app
from app.db import db


@pytest.fixture(scope="function")
def app():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })

    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def setup_db(app):
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="function")
def test_client(app, setup_db):
    return app.test_client()