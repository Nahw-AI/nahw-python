from __future__ import annotations

from pathlib import Path
from typing import Any

from nahw._base import BaseResource
from nahw._types import Report


class ReportsResource(BaseResource):

    def create(self, project_id: str, type: str) -> Report:
        return self._post(
            f"/projects/{project_id}/report", json={"type": type}
        )

    def get_status(self, project_id: str) -> Report:
        return self._get(f"/projects/{project_id}/report-status")

    def list(self, project_id: str) -> list[Report]:
        return self._get(f"/projects/{project_id}/reports")

    def download(self, id: str, dest: str | Path) -> Path:
        dest = Path(dest)
        response = self._client.get(f"/reports/{id}/download")
        response.raise_for_status()
        dest.write_bytes(response.content)
        return dest
