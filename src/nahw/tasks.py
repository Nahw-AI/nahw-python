from __future__ import annotations

from typing import Any

from nahw._base import BaseResource
from nahw._types import PaginatedTasks, Task


class TasksResource(BaseResource):

    def list(
        self,
        project_id: str,
        *,
        page: int = 1,
        limit: int = 50,
        complete: bool | None = None,
        gold: bool | None = None,
    ) -> PaginatedTasks:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if complete is not None:
            params["complete"] = str(complete).lower()
        if gold is not None:
            params["gold"] = str(gold).lower()
        return self._get(f"/projects/{project_id}/tasks", params=params)

    def get(self, id: str) -> dict[str, Any]:
        return self._get(f"/tasks/{id}")

    def create(
        self,
        project_id: str,
        *,
        fields: dict[str, Any],
        is_gold_standard: bool = False,
        gold_standard_answers: dict[str, Any] | None = None,
        gold_standard_explanations: dict[str, Any] | None = None,
    ) -> Task:
        body: dict[str, Any] = {
            "fields": fields,
            "isGoldStandard": is_gold_standard,
        }
        if gold_standard_answers is not None:
            body["goldStandardAnswers"] = gold_standard_answers
        if gold_standard_explanations is not None:
            body["goldStandardExplanations"] = gold_standard_explanations
        return self._post(f"/projects/{project_id}/tasks", json=body)

    def create_with_response(
        self,
        project_id: str,
        *,
        fields: dict[str, Any],
        response: dict[str, Any],
    ) -> dict[str, Any]:
        body = {"fields": fields, "response": response}
        return self._post(
            f"/projects/{project_id}/tasks/with-response", json=body
        )

    def create_bulk(
        self,
        project_id: str,
        tasks: list[dict[str, Any]],
    ) -> list[Task]:
        return self._post(
            f"/projects/{project_id}/tasks/bulk", json={"tasks": tasks}
        )

    def create_from_csv(
        self,
        project_id: str,
        rows: list[dict[str, Any]],
    ) -> list[Task]:
        return self._post(
            f"/projects/{project_id}/tasks/csv", json={"rows": rows}
        )

    def update(
        self,
        id: str,
        *,
        fields: dict[str, Any] | None = None,
        is_complete: bool | None = None,
    ) -> Task:
        body: dict[str, Any] = {}
        if fields is not None:
            body["fields"] = fields
        if is_complete is not None:
            body["isComplete"] = is_complete
        return self._put(f"/tasks/{id}", json=body)

    def delete(self, id: str) -> None:
        self._delete(f"/tasks/{id}")

    def set_gold_standard(
        self,
        id: str,
        *,
        answers: dict[str, Any],
        explanations: dict[str, Any] | None = None,
    ) -> Task:
        body: dict[str, Any] = {"answers": answers}
        if explanations is not None:
            body["explanations"] = explanations
        return self._post(f"/tasks/{id}/gold-standard", json=body)
