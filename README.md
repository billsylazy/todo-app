# To-Do List App

A simple Flask + SQLite to-do list, structured to grow without a rewrite.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe app.py
```

Then open <http://127.0.0.1:5000>.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Structure

- `todoapp/` — application factory, config, db helpers
- `todoapp/tasks/` — the tasks feature: repository (SQL) + routes (HTTP)
- `todoapp/migrations/` — numbered `.sql` files applied in order via `PRAGMA user_version`
- `tests/` — pytest suite against a temp database

To add a schema change: drop a new `NNN_description.sql` file in `todoapp/migrations/`.
It's applied automatically on next app start.
