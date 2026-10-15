from campusflow.reports import get_summary, get_work_queue
from campusflow.search import search_tickets
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import ALLOWED_CATEGORIES, ALLOWED_URGENCIES, create_ticket
from campusflow.understanding_check import QUESTIONS, score_answers
from campusflow.workflow import assign, change_status, reopen

DB = "tickets.json"
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")

def show(ticket):
    who = ticket.get("assigned_to") or "Unassigned"
    print(f"[{ticket['id']}] {ticket['title']} | {ticket['category']} | {ticket['priority']} | {ticket['status']} | {who}")

def find(tickets, ticket_id):
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if str(ticket.get("id", "")).upper() == wanted:
            return ticket
    raise ValueError(f"No ticket found with ID {wanted}.")

def pick(label, allowed):
    names = {item.casefold(): item for item in allowed}
    while True:
        raw = input(f"{label} (blank = any): ").strip()
        if not raw:
            return None
        if raw.casefold() in names:
            return names[raw.casefold()]
        print("Choose:", ", ".join(allowed))

def run(tickets, action):
    try:
        result = action()
    except ValueError as error:
        print(error)
        return None
    save_tickets(DB, tickets)
    return result

def create(tickets):
    print("Categories:", ", ".join(ALLOWED_CATEGORIES))
    print("Urgencies:", ", ".join(ALLOWED_URGENCIES))
    title = input("Title: ")
    category = input("Category: ")
    urgency = input("Urgency: ")
    raw_affected_users = input("Affected users: ").strip()
    try:
        affected_users = int(raw_affected_users)
    except ValueError:
        print("People affected must be a positive whole number.")
        return
    result = create_ticket(
        tickets,
        title,
        category,
        urgency,
        affected_users,
    )
    if not result["success"]:
        print(result["error"])
        return
    save_tickets(DB, tickets)
    show(result["ticket"])

def queue(tickets):
    rows = get_work_queue(tickets)
    if not rows:
        print("No open tickets.")
    for ticket in rows:
        show(ticket)

def report(tickets):
    data = get_summary(tickets)
    print(f"Total: {data['total']} | Unresolved: {data['unresolved']} | Resolved: {data['resolved']} ({data['resolution_percent']}%)")
    print("Status:", data["by_status"])
    print("Priority:", data["by_priority"])
    print("Category:", data["by_category"])

def search(tickets):
    found = search_tickets(
        tickets,
        input("Title contains (blank = any): "),
        pick("Category", ALLOWED_CATEGORIES),
        pick("Status", STATUSES),
        pick("Priority", PRIORITIES),
    )
    if not found:
        print("No matching tickets.")
    for ticket in found:
        show(ticket)

def add_note(tickets):
    try:
        from campusflow.notes import add_note as add
    except ImportError:
        print("add_note is not ready yet. Your partner owns notes.py.")
        return
    ticket_id = input("Ticket ID: ")
    note = run(tickets, lambda: add(tickets, ticket_id, input("Author: "), input("Message: ")))
    if note:
        print(f"Added {note['note_id']} to {ticket_id.strip().upper()}.")

def view_notes(tickets):
    try:
        notes = sorted((find(tickets, input("Ticket ID: ")).get("notes") or []), key=lambda note: note.get("note_id", ""))
    except ValueError as error:
        print(error)
        return
    if not notes:
        print("No notes.")
    for note in notes:
        print(f"[{note['note_id']}] {note['author']}: {note['message']}")

def quiz(tickets):
    answers = []
    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nQ{number}. {question['prompt']}")
        for letter, text in question["choices"]:
            print(f"  {letter}) {text}")
        while (choice := input("A-D: ").strip().upper()) not in {"A", "B", "C", "D"}:
            print("Enter A, B, C, or D.")
        answers.append(choice)
    print(f"Score: {score_answers(answers)}/6")
    print("Explain two answers. These are not graded.")
    print("1.", input("Explanation 1: ").strip())
    print("2.", input("Explanation 2: ").strip())

def main():
    try:
        tickets = load_tickets(DB)
    except StorageError as error:
        print(error)
        print("The file was not changed.")
        return

    actions = {
        "1": queue,
        "2": create,
        "3": lambda rows: run(rows, lambda: assign(rows, input("Ticket ID: "), input("Staff name: "))),
        "4": lambda rows: run(rows, lambda: change_status(rows, input("Ticket ID: "), input("New status: "))),
        "5": lambda rows: run(rows, lambda: reopen(rows, input("Ticket ID: "))),
        "6": report,
        "7": search,
        "8": add_note,
        "9": view_notes,
        "10": quiz,
    }
    while True:
        print("\n1 Queue  2 Create  3 Assign  4 Status  5 Reopen")
        print("6 Report  7 Search  8 Add note  9 View notes  10 Quiz  11 Exit")
        choice = input("Choice: ").strip()
        if choice == "11":
            save_tickets(DB, tickets)
            print("Saved. Goodbye.")
            break
        if choice not in actions:
            print("Choose 1-11.")
            continue
        actions[choice](tickets)

if __name__ == "__main__":
    main()
