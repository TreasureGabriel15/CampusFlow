import json
from pathlib import Path


class StorageError(ValueError):
    pass


def load_tickets(path):
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Could not read {file_path.name}: file is not valid JSON.") from exc
    if not isinstance(data, list):
        raise StorageError(f"Could not read {file_path.name}: tickets must be a JSON list.")
    return data


def save_tickets(path, tickets):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = file_path.with_name(file_path.name + ".tmp")
    temporary.write_text(json.dumps(tickets, indent=2) + "\n", encoding="utf-8")
    temporary.replace(file_path)