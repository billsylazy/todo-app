from datetime import date

from todoapp.db import get_db


def _clean_due_date(raw):
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw).isoformat()
    except ValueError:
        return None


def list_tasks(status="all"):
    db = get_db()
    query = "SELECT * FROM tasks"
    if status == "active":
        query += " WHERE done = 0"
    elif status == "done":
        query += " WHERE done = 1"
    query += (
        " ORDER BY"
        " CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,"
        " due_date ASC,"
        " created_at DESC,"
        " id DESC"
    )
    return db.execute(query).fetchall()


def add_task(title, due_date=None):
    title = title.strip()
    if not title:
        return None
    db = get_db()
    cursor = db.execute(
        "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
        (title, _clean_due_date(due_date)),
    )
    db.commit()
    return cursor.lastrowid


def set_due_date(task_id, due_date):
    db = get_db()
    task = db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        return False
    db.execute(
        "UPDATE tasks SET due_date = ? WHERE id = ?",
        (_clean_due_date(due_date), task_id),
    )
    db.commit()
    return True


def toggle_task(task_id):
    db = get_db()
    task = db.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        return False

    if task["done"]:
        db.execute(
            "UPDATE tasks SET done = 0, completed_at = NULL WHERE id = ?",
            (task_id,),
        )
    else:
        db.execute(
            "UPDATE tasks SET done = 1, completed_at = datetime('now') WHERE id = ?",
            (task_id,),
        )
    db.commit()
    return True


def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
