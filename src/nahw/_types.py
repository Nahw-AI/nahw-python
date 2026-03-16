from __future__ import annotations

from typing import Any, TypedDict


class Project(TypedDict, total=False):
    id: str
    teamId: str
    name: str
    description: str
    status: str
    config: dict[str, Any]
    instructions: str
    fieldsTemplate: list[dict[str, Any]]
    numWorkersPerTask: int
    paymentPerResponse: float
    callbackUrl: str
    teamsRequired: list[str]
    teamsForbidden: list[str]
    skillsRequired: list[str]
    languagesRequired: list[str]
    createdAt: str
    updatedAt: str
    launchedAt: str | None
    pausedAt: str | None
    completedAt: str | None
    cancelledAt: str | None


class Task(TypedDict, total=False):
    id: str
    projectId: str
    fields: dict[str, Any]
    isComplete: bool
    isGoldStandard: bool
    goldStandardAnswers: dict[str, Any] | None
    goldStandardExplanations: dict[str, Any] | None
    createdAt: str
    updatedAt: str


class TaskResponse(TypedDict, total=False):
    id: str
    taskId: str
    workerId: str
    workerName: str
    data: dict[str, Any]
    status: str
    startedAt: str
    completedAt: str | None
    durationMs: int | None
    isGoldCheck: bool
    goldScore: float | None
    createdAt: str


class Report(TypedDict, total=False):
    id: str
    projectId: str
    type: str
    status: str
    jobId: str | None
    downloadUrl: str | None
    expiresAt: str | None
    rowCount: int | None
    errorMessage: str | None
    createdAt: str


class PaginatedTasks(TypedDict):
    tasks: list[Task]
    total: int
    page: int
    limit: int
