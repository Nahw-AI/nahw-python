from __future__ import annotations


class NahwAPIError(Exception):
    """Base exception for nahw API errors."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")


class NahwValidationError(NahwAPIError):
    """400 Bad Request — invalid input."""


class NahwAuthenticationError(NahwAPIError):
    """401 Unauthorized — missing or invalid API key."""


class NahwAccessDeniedError(NahwAPIError):
    """403 Forbidden — insufficient permissions."""


class NahwNotFoundError(NahwAPIError):
    """404 Not Found — resource does not exist."""


class NahwConflictError(NahwAPIError):
    """409 Conflict — resource state conflict."""


_STATUS_MAP: dict[int, type[NahwAPIError]] = {
    400: NahwValidationError,
    401: NahwAuthenticationError,
    403: NahwAccessDeniedError,
    404: NahwNotFoundError,
    409: NahwConflictError,
}


def raise_for_status(status_code: int, body: dict | str) -> None:
    """Raise typed exception for non-2xx status codes."""
    if 200 <= status_code < 300:
        return
    if isinstance(body, dict):
        message = body.get("message") or body.get("error") or str(body)
    else:
        message = str(body)
    exc_class = _STATUS_MAP.get(status_code, NahwAPIError)
    raise exc_class(status_code, message)
