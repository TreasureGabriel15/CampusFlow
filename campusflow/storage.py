import json
import re
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

    
    seen_ids = set()
    for index, ticket in enumerate(data):
        if not isinstance(ticket, dict):
            raise StorageError(
                f"Could not read {file_path.name}: ticket {index + 1} must be a JSON object."
            )
        ticket_id = ticket.get("id")
        if not isinstance(ticket_id, str) or not re.fullmatch(r"T\d+", ticket_id, re.IGNORECASE):
            raise StorageError(
                f"Could not read {file_path.name}: ticket {index + 1} has an invalid ID."
            )
        normalized_id = ticket_id.upper()
        if normalized_id in seen_ids:
            raise StorageError(
                f"Could not read {file_path.name}: duplicate ticket ID {normalized_id}."
            )
        seen_ids.add(normalized_id)
    return data


def save_tickets(path, tickets):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = file_path.with_name(file_path.name + ".tmp")
    temporary.write_text(json.dumps(tickets, indent=2) + "\n", encoding="utf-8")
    temporary.replace(file_path)