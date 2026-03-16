from __future__ import annotations

from typing import Any

import httpx

from nahw._exceptions import raise_for_status


class BaseResource:
    """Shared HTTP helpers for all resource classes."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self._client.request(method, path, **kwargs)
        if response.status_code == 204:
            return None
        try:
            body = response.json()
        except Exception:
            body = response.text
        raise_for_status(response.status_code, body)
        return body

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: Any | None = None) -> Any:
        return self._request("POST", path, json=json)

    def _patch(self, path: str, json: Any | None = None) -> Any:
        return self._request("PATCH", path, json=json)

    def _put(self, path: str, json: Any | None = None) -> Any:
        return self._request("PUT", path, json=json)

    def _delete(self, path: str) -> Any:
        return self._request("DELETE", path)
