def test_empty_list(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No tasks yet" in response.data


def test_add_task_persists(client):
    client.post("/tasks", data={"title": "Buy groceries"})
    response = client.get("/")
    assert b"Buy groceries" in response.data


def test_add_blank_task_rejected(client):
    client.post("/tasks", data={"title": "   "})
    response = client.get("/")
    assert b"can&#39;t be empty" in response.data or b"can't be empty" in response.data
    assert b"No tasks yet" in response.data


def test_toggle_task(client):
    client.post("/tasks", data={"title": "Call the bank"})
    response = client.get("/")
    task_id = _extract_task_id(response.data)

    client.post(f"/tasks/{task_id}/toggle")
    response = client.get("/?status=done")
    assert b"Call the bank" in response.data

    response = client.get("/?status=active")
    assert b"Call the bank" not in response.data


def test_delete_task(client):
    client.post("/tasks", data={"title": "Ship the report"})
    response = client.get("/")
    task_id = _extract_task_id(response.data)

    client.post(f"/tasks/{task_id}/delete")
    response = client.get("/")
    assert b"Ship the report" not in response.data
    assert b"No tasks yet" in response.data


def test_add_task_with_due_date(client):
    client.post("/tasks", data={"title": "Pay rent", "due_date": "2026-08-01"})
    response = client.get("/")
    assert b"2026-08-01" in response.data


def test_invalid_due_date_ignored_not_crashed(client):
    response = client.post(
        "/tasks", data={"title": "Bad date", "due_date": "not-a-date"}
    )
    assert response.status_code == 302
    response = client.get("/")
    assert b"Bad date" in response.data


def test_update_due_date(client):
    client.post("/tasks", data={"title": "Renew license"})
    response = client.get("/")
    task_id = _extract_task_id(response.data)

    client.post(f"/tasks/{task_id}/due-date", data={"due_date": "2026-09-01"})
    response = client.get("/")
    assert b"2026-09-01" in response.data


def test_tasks_with_due_date_sort_before_tasks_without(client):
    client.post("/tasks", data={"title": "No date"})
    client.post("/tasks", data={"title": "Has date", "due_date": "2026-08-01"})
    html = client.get("/").data.decode()
    assert html.index("Has date") < html.index("No date")


def _extract_task_id(html_bytes):
    html = html_bytes.decode()
    marker = "/tasks/"
    start = html.index(marker) + len(marker)
    end = html.index("/", start)
    return html[start:end]
