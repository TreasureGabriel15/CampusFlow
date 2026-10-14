def search_tickets(tickets, title="", category=None, status=None, priority=None):
    query = str(title).strip().casefold()

    def same(value, expected):
        if not expected:
            return True
        return str(value).strip().casefold() == str(expected).strip().casefold()

    found = []
    for ticket in tickets:
        if query and query not in str(ticket.get("title", "")).casefold():
            continue
        if not same(ticket.get("category"), category):
            continue
        if not same(ticket.get("status"), status):
            continue
        if not same(ticket.get("priority"), priority):
            continue
        found.append(ticket)
    return found