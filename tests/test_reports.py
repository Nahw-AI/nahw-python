import httpx

REPORT = {
    "id": "rpt_1",
    "projectId": "proj_1",
    "type": "json",
    "status": "completed",
    "downloadUrl": "https://cdn.nahw.ai/rpt_1.json",
}


def test_create(mock_api, client):
    mock_api.post("/projects/proj_1/report").mock(
        return_value=httpx.Response(201, json=REPORT)
    )
    result = client.reports.create("proj_1", type="json")
    assert result["type"] == "json"


def test_get_status(mock_api, client):
    mock_api.get("/projects/proj_1/report-status").mock(
        return_value=httpx.Response(200, json=REPORT)
    )
    result = client.reports.get_status("proj_1")
    assert result["status"] == "completed"


def test_list(mock_api, client):
    mock_api.get("/projects/proj_1/reports").mock(
        return_value=httpx.Response(200, json=[REPORT])
    )
    result = client.reports.list("proj_1")
    assert len(result) == 1


def test_download(mock_api, client, tmp_path):
    mock_api.get("/reports/rpt_1/download").mock(
        return_value=httpx.Response(200, content=b'{"rows": []}')
    )
    dest = tmp_path / "report.json"
    path = client.reports.download("rpt_1", dest)
    assert path.read_text() == '{"rows": []}'
