# nahw-python

Python SDK for the [nahw-ai](https://nahw.ai) REST API.

## Installation

```bash
pip install nahw-python
```

Or install from source:

```bash
pip install git+https://github.com/Nahw-AI/nahw-python.git
```

**Requires Python 3.10+**

## Quick Start

```python
from nahw import NahwClient

client = NahwClient(api_key="nhw_...")

# List projects
projects = client.projects.list()

# Create a project
project = client.projects.create(
    "My Project",
    instructions="Label the sentiment of each text.",
    num_workers_per_task=3,
    payment_per_response=0.10,
)

# Add tasks
client.tasks.create(project["id"], fields={"text": "I love this product!"})

# Bulk create (up to 10k)
client.tasks.create_bulk(project["id"], [
    {"fields": {"text": "Great service"}},
    {"fields": {"text": "Terrible experience"}},
])

# Launch
client.projects.launch(project["id"])
```

## Configuration

```python
client = NahwClient(
    api_key="nhw_...",
    base_url="https://api.nahw.ai",  # default
    team_id="team_123",              # optional, sets X-Team-Id header
    timeout=30.0,                    # request timeout in seconds
)
```

The client supports context manager usage:

```python
with NahwClient(api_key="nhw_...") as client:
    projects = client.projects.list()
```

## Resources

### Projects

```python
client.projects.list(page=1, statuses=["active", "paused"])
client.projects.list_shared()
client.projects.get("proj_123")
client.projects.create("Name", description="...", instructions="...")
client.projects.update("proj_123", name="New Name")
client.projects.delete("proj_123")

# Lifecycle
client.projects.launch("proj_123")    # draft → active
client.projects.pause("proj_123")     # active → paused
client.projects.resume("proj_123")    # paused → active
client.projects.complete("proj_123")  # → completed
client.projects.cancel("proj_123")    # → cancelled

# Other
client.projects.clone("proj_123", name="Copy")
client.projects.check_eligibility("proj_123", "worker_456")
```

### Tasks

```python
client.tasks.list("proj_123", page=1, limit=50, complete=False, gold=True)
client.tasks.get("task_123")
client.tasks.create("proj_123", fields={"text": "Hello"})
client.tasks.create_with_response("proj_123", fields={...}, response={...})
client.tasks.create_bulk("proj_123", [{"fields": {...}}, ...])
client.tasks.create_from_csv("proj_123", [{"col1": "val1"}, ...])
client.tasks.update("task_123", is_complete=True)
client.tasks.delete("task_123")
client.tasks.set_gold_standard("task_123", answers={"q1": "a1"})
```

### Responses

```python
client.responses.list("task_123")
client.responses.submit("resp_123", data={"answer": "42"}, duration_ms=5000)
```

### Reports

```python
client.reports.create("proj_123", type="json")       # also: csv, csv_aggregated, csv_flattened
client.reports.get_status("proj_123")
client.reports.list("proj_123")
client.reports.download("rpt_123", "output.json")
```

## Error Handling

All API errors raise typed exceptions:

```python
from nahw import (
    NahwAPIError,
    NahwValidationError,       # 400
    NahwAuthenticationError,   # 401
    NahwAccessDeniedError,     # 403
    NahwNotFoundError,         # 404
    NahwConflictError,         # 409
)

try:
    client.projects.get("nonexistent")
except NahwNotFoundError as e:
    print(e.status_code)  # 404
    print(e.message)
except NahwAPIError as e:
    print(f"Unexpected error: {e}")
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```
