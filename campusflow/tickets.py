from campusflow.validation import (
    ALLOWED_CATEGORIES,
    ALLOWED_URGENCIES,
    validate_affected_users,
    validate_category,
    validate_title,
    validate_urgency,
)


def calculate_priority(urgency, affected_users):
    """
    Rules (first match wins):
    1. high urgency AND >= 10 users  -> critical
    2. high urgency OR  >= 10 users  -> high
    3. medium urgency OR >= 3 users  -> medium
    4. everything else                -> low
    """
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def next_ticket_id(tickets):
    if not tickets:
        return "T001"
    numbers = []
    for t in tickets:
        numbers.append(int(t["id"][1:]))
    return f"T{max(numbers) + 1:03d}"

def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None


def create_ticket(tickets, title, category, urgency, affected_users):
    try:
        title = validate_title(title)
        category = validate_category(category)
        urgency = validate_urgency(urgency)
        affected_users = validate_affected_users(affected_users)
    except ValueError as error:
        return {"success": False, "error": str(error)}

    priority = calculate_priority(urgency, affected_users)
    new_id = next_ticket_id(tickets)

    ticket = {
        "id": new_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }
    tickets.append(ticket)
    return {"success": True, "ticket": ticket}
