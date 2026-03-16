import httpx

RESPONSE = {
    "id": "resp_1",
    "taskId": "task_1",
    "workerId": "worker_1",
    "workerName": "Alice",
    "data": {"answer": "42"},
    "status": "completed",
}


def test_list(mock_api, client):
    mock_api.get("/tasks/task_1/responses").mock(
        return_value=httpx.Response(200, json=[RESPONSE])
    )
    result = client.responses.list("task_1")
    assert len(result) == 1
    assert result[0]["id"] == "resp_1"


def test_submit(mock_api, client):
    mock_api.post("/task-responses/resp_1/submit").mock(
        return_value=httpx.Response(200, json=RESPONSE)
    )
    result = client.responses.submit(
        "resp_1", data={"answer": "42"}, duration_ms=5000
    )
    assert result["status"] == "completed"
