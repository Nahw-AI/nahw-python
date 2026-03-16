from __future__ import annotations

from typing import Any

from nahw._base import BaseResource
from nahw._types import TaskResponse


class ResponsesResource(BaseResource):

    def list(self, task_id: str) -> list[TaskResponse]:
        return self._get(f"/tasks/{task_id}/responses")

    def submit(
        self,
        id: str,
        *,
        data: dict[str, Any],
        duration_ms: int | None = None,
    ) -> TaskResponse:
        body: dict[str, Any] = {"data": data}
        if duration_ms is not None:
            body["durationMs"] = duration_ms
        return self._post(f"/task-responses/{id}/submit", json=body)
