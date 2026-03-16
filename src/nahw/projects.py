from __future__ import annotations

from typing import Any

from nahw._base import BaseResource
from nahw._types import Project


class ProjectsResource(BaseResource):

    def list(
        self,
        *,
        page: int | None = None,
        statuses: list[str] | None = None,
    ) -> list[Project]:
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if statuses is not None:
            params["statuses"] = ",".join(statuses)
        return self._get("/projects", params=params or None)

    def list_shared(self) -> list[Project]:
        return self._get("/projects/shared")

    def get(self, id: str) -> Project:
        return self._get(f"/projects/{id}")

    def create(
        self,
        name: str,
        *,
        description: str | None = None,
        config: dict[str, Any] | None = None,
        instructions: str | None = None,
        fields_template: list[dict[str, Any]] | None = None,
        num_workers_per_task: int | None = None,
        payment_per_response: float | None = None,
        callback_url: str | None = None,
        teams_required: list[str] | None = None,
        teams_forbidden: list[str] | None = None,
        skills_required: list[str] | None = None,
        languages_required: list[str] | None = None,
    ) -> Project:
        body: dict[str, Any] = {"name": name}
        _set_optional(body, "description", description)
        _set_optional(body, "config", config)
        _set_optional(body, "instructions", instructions)
        _set_optional(body, "fieldsTemplate", fields_template)
        _set_optional(body, "numWorkersPerTask", num_workers_per_task)
        _set_optional(body, "paymentPerResponse", payment_per_response)
        _set_optional(body, "callbackUrl", callback_url)
        _set_optional(body, "teamsRequired", teams_required)
        _set_optional(body, "teamsForbidden", teams_forbidden)
        _set_optional(body, "skillsRequired", skills_required)
        _set_optional(body, "languagesRequired", languages_required)
        return self._post("/projects", json=body)

    def update(self, id: str, **kwargs: Any) -> Project:
        body: dict[str, Any] = {}
        key_map = {
            "name": "name",
            "description": "description",
            "config": "config",
            "instructions": "instructions",
            "fields_template": "fieldsTemplate",
            "num_workers_per_task": "numWorkersPerTask",
            "payment_per_response": "paymentPerResponse",
            "callback_url": "callbackUrl",
            "teams_required": "teamsRequired",
            "teams_forbidden": "teamsForbidden",
            "skills_required": "skillsRequired",
            "languages_required": "languagesRequired",
        }
        for py_key, api_key in key_map.items():
            if py_key in kwargs:
                body[api_key] = kwargs[py_key]
        return self._patch(f"/projects/{id}", json=body)

    def delete(self, id: str) -> None:
        self._delete(f"/projects/{id}")

    def launch(self, id: str) -> Project:
        return self._put(f"/projects/{id}/launch")

    def pause(self, id: str) -> Project:
        return self._put(f"/projects/{id}/pause")

    def resume(self, id: str) -> Project:
        return self._put(f"/projects/{id}/resume")

    def complete(self, id: str) -> Project:
        return self._put(f"/projects/{id}/complete")

    def cancel(self, id: str) -> Project:
        return self._put(f"/projects/{id}/cancel")

    def clone(
        self,
        id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        _set_optional(body, "name", name)
        _set_optional(body, "description", description)
        return self._post(f"/projects/{id}/clone", json=body or None)

    def check_eligibility(self, id: str, worker_id: str) -> dict[str, Any]:
        return self._get(f"/projects/{id}/eligible/{worker_id}")


def _set_optional(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value
