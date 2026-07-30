import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    DB_PATH = os.environ.get("TODO_DB", str(BASE_DIR / "todo.db"))


class TestConfig(Config):
    TESTING = True
    DB_PATH = ":memory:"
