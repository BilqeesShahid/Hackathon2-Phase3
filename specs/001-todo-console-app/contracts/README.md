# Contracts: Todo In-Memory Python Console Application

**Note**: This is a CLI application with no external API contracts.

The application uses direct function calls between modules:

- `main.py` → `task_service.py` (function calls)
- `task_service.py` → `task.py` (dataclass instantiation)

No network protocols, HTTP endpoints, or IPC mechanisms are used.

For data structures, see [data-model.md](../data-model.md).
