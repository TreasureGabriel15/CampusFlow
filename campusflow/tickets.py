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


ALLOWED_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
ALLOWED_URGENCIES = ["low", "medium", "high"]


def create_ticket(tickets, title, category, urgency, affected_users):
 
    title = str(title).strip()
    if not title:
        return {"success": False, "error": "Title cannot be blank"}
    category = str(category).strip().capitalize()
    if category not in ALLOWED_CATEGORIES:
        return {
            "success": False,
            "error": f"Category must be one of {ALLOWED_CATEGORIES}"
        }
    urgency = str(urgency).strip().lower()
    if urgency not in ALLOWED_URGENCIES:
        return {
            "success": False,
            "error": f"Urgency must be one of {ALLOWED_URGENCIES}"
        }
    try:
        affected_users = int(affected_users)
    except (ValueError, TypeError):
        return {"success": False, "error": "People affected must be a whole number"}
    if affected_users <= 0:
        return {"success": False, "error": "People affected must be positive"}

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
    }
    tickets.append(ticket)
    return {"success": True, "ticket": ticket}
