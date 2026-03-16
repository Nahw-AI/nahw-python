import httpx

TASK = {
    "id": "task_1",
    "projectId": "proj_1",
    "fields": {"text": "hello"},
    "isComplete": False,
    "isGoldStandard": False,
}

PAGINATED = {"tasks": [TASK], "total": 1, "page": 1, "limit": 50}


def test_list(mock_api, client):
    mock_api.get("/projects/proj_1/tasks").mock(
        return_value=httpx.Response(200, json=PAGINATED)
    )
    result = client.tasks.list("proj_1")
    assert result["total"] == 1
    assert len(result["tasks"]) == 1


def test_list_with_filters(mock_api, client):
    mock_api.get(
        "/projects/proj_1/tasks",
        params={"page": "2", "limit": "10", "complete": "true"},
    ).mock(return_value=httpx.Response(200, json=PAGINATED))
    client.tasks.list("proj_1", page=2, limit=10, complete=True)


def test_get(mock_api, client):
    mock_api.get("/tasks/task_1").mock(
        return_value=httpx.Response(
            200, json={**TASK, "responses": []}
        )
    )
    result = client.tasks.get("task_1")
    assert result["id"] == "task_1"


def test_create(mock_api, client):
    mock_api.post("/projects/proj_1/tasks").mock(
        return_value=httpx.Response(201, json=TASK)
    )
    result = client.tasks.create("proj_1", fields={"text": "hello"})
    assert result["id"] == "task_1"


def test_create_with_response(mock_api, client):
    mock_api.post("/projects/proj_1/tasks/with-response").mock(
        return_value=httpx.Response(
            201, json={"task": TASK, "response": {"id": "resp_1"}}
        )
    )
    result = client.tasks.create_with_response(
        "proj_1",
        fields={"text": "hello"},
        response={"answer": "world"},
    )
    assert "task" in result


def test_create_bulk(mock_api, client):
    mock_api.post("/projects/proj_1/tasks/bulk").mock(
        return_value=httpx.Response(201, json=[TASK])
    )
    result = client.tasks.create_bulk(
        "proj_1", [{"fields": {"text": "hello"}}]
    )
    assert len(result) == 1


def test_create_from_csv(mock_api, client):
    mock_api.post("/projects/proj_1/tasks/csv").mock(
        return_value=httpx.Response(201, json=[TASK])
    )
    result = client.tasks.create_from_csv("proj_1", [{"text": "hello"}])
    assert len(result) == 1


def test_update(mock_api, client):
    mock_api.put("/tasks/task_1").mock(
        return_value=httpx.Response(
            200, json={**TASK, "isComplete": True}
        )
    )
    result = client.tasks.update("task_1", is_complete=True)
    assert result["isComplete"] is True


def test_delete(mock_api, client):
    mock_api.delete("/tasks/task_1").mock(
        return_value=httpx.Response(204)
    )
    client.tasks.delete("task_1")


def test_set_gold_standard(mock_api, client):
    mock_api.post("/tasks/task_1/gold-standard").mock(
        return_value=httpx.Response(
            200, json={**TASK, "isGoldStandard": True}
        )
    )
    result = client.tasks.set_gold_standard(
        "task_1", answers={"q1": "a1"}
    )
    assert result["isGoldStandard"] is True
