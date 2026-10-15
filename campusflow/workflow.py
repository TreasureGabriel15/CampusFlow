from campusflow.validation import validate_staff_name, validate_status


_NEXT = {"open": "in_progress", "in_progress": "resolved"}

def _find(tickets, ticket_id):
    wanted = str(ticket_id or "").strip().upper()
    if not wanted:
        raise ValueError("Ticket ID is required.")
    for ticket in tickets:
        if str(ticket.get("id", "")).strip().upper() == wanted:
            return ticket
    raise ValueError(f"No ticket found with ID {wanted}.")

def _unlocked(ticket):
    if ticket.get("status") == "resolved":
        raise ValueError("Resolved ticket is locked. Reopen it first.")

def assign(tickets, ticket_id, staff_name):
    ticket = _find(tickets, ticket_id)
    _unlocked(ticket)
    ticket["assigned_to"] = validate_staff_name(staff_name)
    return ticket

def change_status(tickets, ticket_id, new_status):
    ticket = _find(tickets, ticket_id)
    _unlocked(ticket)
    status = validate_status(new_status)
    if _NEXT.get(ticket.get("status")) != status:
        raise ValueError(f"Cannot move '{ticket.get('status')}' straight to '{status}'.")
    if status == "in_progress" and not str(ticket.get("assigned_to") or "").strip():
        raise ValueError("Assign the ticket before moving it to in_progress.")
    ticket["status"] = status
    return ticket

def reopen(tickets, ticket_id):
    ticket = _find(tickets, ticket_id)
    if ticket.get("status") != "resolved":
        raise ValueError("Only a resolved ticket can be reopened.")
    ticket["status"] = "open"
    return ticket