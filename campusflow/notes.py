def _next_note_id(ticket):
    numbers = []
    for note in ticket.get("notes") or []:
        note_id = note.get("note_id", "")
        if isinstance(note_id, str) and note_id.startswith("N") and note_id[1:].isdigit():
            numbers.append(int(note_id[1:]))
    return f"N{max(numbers, default=0) + 1:03d}"


def add_note(tickets, ticket_id, author, message):
    wanted = str(ticket_id or "").strip().upper()
    if not wanted:
        raise ValueError("Ticket ID is required.")

    ticket = next(
        (row for row in tickets if str(row.get("id", "")).strip().upper() == wanted),
        None,
    )
    if ticket is None:
        raise ValueError(f"No ticket found with ID {wanted}.")
    if ticket.get("status") == "resolved":
        raise ValueError("Resolved ticket is locked. Reopen it first.")

    author = author.strip() if isinstance(author, str) else ""
    message = message.strip() if isinstance(message, str) else ""
    if not author:
        raise ValueError("Note author cannot be blank.")
    if not message:
        raise ValueError("Note message cannot be blank.")
    if not 5 <= len(message) <= 300:
        raise ValueError("Note message must be between 5 and 300 characters.")

    note = {
        "note_id": _next_note_id(ticket),
        "author": author,
        "message": message,
    }
    ticket.setdefault("notes", []).append(note)
    return note
