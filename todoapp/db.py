import sqlite3
from pathlib import Path

from flask import current_app, g

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def run_migrations():
    db = get_db()
    current_version = db.execute("PRAGMA user_version").fetchone()[0]

    migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for path in migrations:
        version = int(path.name.split("_", 1)[0])
        if version <= current_version:
            continue
        db.executescript(path.read_text())
        db.execute(f"PRAGMA user_version = {version}")
        db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
