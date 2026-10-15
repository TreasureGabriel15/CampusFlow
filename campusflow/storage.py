import json
import re
from pathlib import Path

from campusflow.tickets import (
    ALLOWED_CATEGORIES,
    ALLOWED_URGENCIES,
    calculate_priority,
)


class StorageError(ValueError):
    pass


def _validate_tickets(data, filename):
    seen_ids = set()
    validated = []
    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    }
    allowed_statuses = {"open", "in_progress", "resolved"}

    for index, ticket in enumerate(data):
        if not isinstance(ticket, dict):
            raise StorageError(
                f"Could not read {filename}: ticket {index + 1} must be a JSON object."
            )

        missing_fields = required_fields - ticket.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise StorageError(
                f"Could not read {filename}: ticket {index + 1} is missing {missing}."
            )

        ticket_id = ticket["id"]
        if not isinstance(ticket_id, str) or not re.fullmatch(r"T\d+", ticket_id, re.IGNORECASE):
            raise StorageError(
                f"Could not read {filename}: ticket {index + 1} has an invalid ID."
            )
        normalized_id = ticket_id.upper()
        if normalized_id in seen_ids:
            raise StorageError(
                f"Could not read {filename}: duplicate ticket ID {normalized_id}."
            )
        seen_ids.add(normalized_id)

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has an invalid title."
            )
        if ticket["category"] not in ALLOWED_CATEGORIES:
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has an invalid category."
            )
        if ticket["urgency"] not in ALLOWED_URGENCIES:
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has an invalid urgency."
            )

        affected_users = ticket["affected_users"]
        if isinstance(affected_users, bool) or not isinstance(affected_users, int) or affected_users <= 0:
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has invalid affected_users."
            )
        expected_priority = calculate_priority(ticket["urgency"], affected_users)
        if ticket["priority"] != expected_priority:
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has inconsistent priority."
            )
        if not isinstance(ticket["status"], str) or ticket["status"] not in allowed_statuses:
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has an invalid status."
            )
        assigned_to = ticket["assigned_to"]
        if assigned_to is not None and (
            not isinstance(assigned_to, str) or not assigned_to.strip()
        ):
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} has an invalid assignee."
            )

        ticket_copy = ticket.copy()
        notes = ticket_copy.setdefault("notes", [])
        if not isinstance(notes, list):
            raise StorageError(
                f"Could not read {filename}: ticket {normalized_id} notes must be a JSON list."
            )
        seen_note_ids = set()
        for note_index, note in enumerate(notes):
            if not isinstance(note, dict):
                raise StorageError(
                    f"Could not read {filename}: note {note_index + 1} on {normalized_id} must be a JSON object."
                )
            if not {"note_id", "author", "message"} <= note.keys():
                raise StorageError(
                    f"Could not read {filename}: note {note_index + 1} on {normalized_id} is missing required fields."
                )
            note_id = note["note_id"]
            if not isinstance(note_id, str) or not re.fullmatch(r"N\d+", note_id, re.IGNORECASE):
                raise StorageError(
                    f"Could not read {filename}: note {note_index + 1} on {normalized_id} has an invalid ID."
                )
            normalized_note_id = note_id.upper()
            if normalized_note_id in seen_note_ids:
                raise StorageError(
                    f"Could not read {filename}: duplicate note ID {normalized_note_id} on {normalized_id}."
                )
            seen_note_ids.add(normalized_note_id)
            if not isinstance(note["author"], str) or not note["author"].strip():
                raise StorageError(
                    f"Could not read {filename}: note {normalized_note_id} on {normalized_id} has an invalid author."
                )
            message = note["message"]
            if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
                raise StorageError(
                    f"Could not read {filename}: note {normalized_note_id} on {normalized_id} has an invalid message."
                )
        validated.append(ticket_copy)

    return validated


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

    return _validate_tickets(data, file_path.name)


def save_tickets(path, tickets):
    validated = _validate_tickets(tickets, Path(path).name)
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = file_path.with_name(file_path.name + ".tmp")
    temporary.write_text(json.dumps(validated, indent=2) + "\n", encoding="utf-8")
    temporary.replace(file_path)