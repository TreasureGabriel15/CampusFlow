_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _number(ticket):
    digits = "".join(ch for ch in str(ticket.get("id", "")) if ch.isdigit())
    return int(digits) if digits else 10**9


def get_work_queue(tickets):
    waiting = [ticket for ticket in tickets if ticket.get("status") != "resolved"]
    return sorted(waiting, key=lambda ticket: (_RANK.get(ticket.get("priority"), 99), _number(ticket)))


def get_summary(tickets):
    by_status = {"open": 0, "in_progress": 0, "resolved": 0}
    by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for ticket in tickets:
        if ticket.get("status") in by_status:
            by_status[ticket["status"]] += 1
        if ticket.get("priority") in by_priority:
            by_priority[ticket["priority"]] += 1
    return {"total": len(tickets), "by_status": by_status, "by_priority": by_priority}