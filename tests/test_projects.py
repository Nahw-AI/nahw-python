import httpx
import respx

PROJECT = {
    "id": "proj_1",
    "teamId": "team_1",
    "name": "Test Project",
    "status": "draft",
}


def test_list(mock_api, client):
    mock_api.get("/projects").mock(
        return_value=httpx.Response(200, json=[PROJECT])
    )
    result = client.projects.list()
    assert result == [PROJECT]


def test_list_with_filters(mock_api, client):
    mock_api.get("/projects", params={"statuses": "active,paused"}).mock(
        return_value=httpx.Response(200, json=[])
    )
    result = client.projects.list(statuses=["active", "paused"])
    assert result == []


def test_list_shared(mock_api, client):
    mock_api.get("/projects/shared").mock(
        return_value=httpx.Response(200, json=[PROJECT])
    )
    assert client.projects.list_shared() == [PROJECT]


def test_get(mock_api, client):
    mock_api.get("/projects/proj_1").mock(
        return_value=httpx.Response(200, json=PROJECT)
    )
    assert client.projects.get("proj_1") == PROJECT


def test_create(mock_api, client):
    route = mock_api.post("/projects").mock(
        return_value=httpx.Response(201, json=PROJECT)
    )
    result = client.projects.create(
        "Test Project", description="desc", num_workers_per_task=3
    )
    assert result == PROJECT
    body = route.calls[0].request.content
    import json

    sent = json.loads(body)
    assert sent["name"] == "Test Project"
    assert sent["description"] == "desc"
    assert sent["numWorkersPerTask"] == 3


def test_update(mock_api, client):
    updated = {**PROJECT, "name": "New Name"}
    mock_api.patch("/projects/proj_1").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = client.projects.update("proj_1", name="New Name")
    assert result["name"] == "New Name"


def test_delete(mock_api, client):
    mock_api.delete("/projects/proj_1").mock(
        return_value=httpx.Response(204)
    )
    client.projects.delete("proj_1")


def test_launch(mock_api, client):
    launched = {**PROJECT, "status": "active"}
    mock_api.put("/projects/proj_1/launch").mock(
        return_value=httpx.Response(200, json=launched)
    )
    assert client.projects.launch("proj_1")["status"] == "active"


def test_pause(mock_api, client):
    mock_api.put("/projects/proj_1/pause").mock(
        return_value=httpx.Response(200, json={**PROJECT, "status": "paused"})
    )
    assert client.projects.pause("proj_1")["status"] == "paused"


def test_resume(mock_api, client):
    mock_api.put("/projects/proj_1/resume").mock(
        return_value=httpx.Response(200, json={**PROJECT, "status": "active"})
    )
    assert client.projects.resume("proj_1")["status"] == "active"


def test_complete(mock_api, client):
    mock_api.put("/projects/proj_1/complete").mock(
        return_value=httpx.Response(
            200, json={**PROJECT, "status": "completed"}
        )
    )
    assert client.projects.complete("proj_1")["status"] == "completed"


def test_cancel(mock_api, client):
    mock_api.put("/projects/proj_1/cancel").mock(
        return_value=httpx.Response(
            200, json={**PROJECT, "status": "cancelled"}
        )
    )
    assert client.projects.cancel("proj_1")["status"] == "cancelled"


def test_clone(mock_api, client):
    mock_api.post("/projects/proj_1/clone").mock(
        return_value=httpx.Response(
            201, json={"project": {**PROJECT, "id": "proj_2"}, "questions": []}
        )
    )
    result = client.projects.clone("proj_1", name="Cloned")
    assert result["project"]["id"] == "proj_2"


def test_check_eligibility(mock_api, client):
    mock_api.get("/projects/proj_1/eligible/worker_1").mock(
        return_value=httpx.Response(200, json={"eligible": True})
    )
    result = client.projects.check_eligibility("proj_1", "worker_1")
    assert result["eligible"] is True
