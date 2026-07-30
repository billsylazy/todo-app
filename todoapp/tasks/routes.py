from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from todoapp.tasks import repository

bp = Blueprint("tasks", __name__)


@bp.route("/")
def index():
    status = request.args.get("status", "all")
    if status not in ("all", "active", "done"):
        status = "all"
    tasks = repository.list_tasks(status)
    return render_template(
        "tasks/index.html", tasks=tasks, status=status, today=date.today().isoformat()
    )


@bp.route("/tasks", methods=["POST"])
def create():
    title = request.form.get("title", "")
    due_date = request.form.get("due_date", "")
    task_id = repository.add_task(title, due_date)
    if task_id is None:
        flash("Task title can't be empty.")
    return redirect(url_for("tasks.index"))


@bp.route("/tasks/<int:task_id>/due-date", methods=["POST"])
def update_due_date(task_id):
    due_date = request.form.get("due_date", "")
    repository.set_due_date(task_id, due_date)
    return redirect(url_for("tasks.index", status=request.args.get("status", "all")))


@bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id):
    repository.toggle_task(task_id)
    return redirect(url_for("tasks.index", status=request.args.get("status", "all")))


@bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete(task_id):
    repository.delete_task(task_id)
    return redirect(url_for("tasks.index", status=request.args.get("status", "all")))
