from __future__ import annotations

import httpx

from nahw.projects import ProjectsResource
from nahw.reports import ReportsResource
from nahw.responses import ResponsesResource
from nahw.tasks import TasksResource

_DEFAULT_BASE_URL = "https://api.nahw.ai"


class NahwClient:
    """Main entry point for the nahw API SDK."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        team_id: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        headers: dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
        }
        if team_id is not None:
            headers["X-Team-Id"] = team_id

        self._http = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )
        self._projects: ProjectsResource | None = None
        self._tasks: TasksResource | None = None
        self._responses: ResponsesResource | None = None
        self._reports: ReportsResource | None = None

    # Lazy resource properties

    @property
    def projects(self) -> ProjectsResource:
        if self._projects is None:
            self._projects = ProjectsResource(self._http)
        return self._projects

    @property
    def tasks(self) -> TasksResource:
        if self._tasks is None:
            self._tasks = TasksResource(self._http)
        return self._tasks

    @property
    def responses(self) -> ResponsesResource:
        if self._responses is None:
            self._responses = ResponsesResource(self._http)
        return self._responses

    @property
    def reports(self) -> ReportsResource:
        if self._reports is None:
            self._reports = ReportsResource(self._http)
        return self._reports

    # Context manager

    def __enter__(self) -> NahwClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()
