import pytest

from todoapp import create_app
from todoapp.config import TestConfig


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(TestConfig, DB_PATH=str(db_path))
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
