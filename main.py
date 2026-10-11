import sys
# The fix: Adding 'campusflow.' prefix so python finds the files inside the folder
from campusflow.tickets import create_ticket, ALLOWED_CATEGORIES, ALLOWED_URGENCIES
from campusflow.workflow import assign, change_status, reopen
from campusflow.reports import get_work_queue, get_summary
from campusflow.storage import load_tickets, save_tickets, StorageError

DB_FILE = "tickets.json"

def print_header(title):
    print(f"\n=== {title.upper()} ===")

def view_queue(tickets):
    print_header("Work Queue (Sorted by Priority & ID)")
    queue = get_work_queue(tickets)
    if not queue:
        print("No unresolved tickets found.")
        return
    for t in queue:
        print(f"[{t['id']}] {t['title']} | Priority: {t['priority'].upper()} | Status: {t['status']} | Assigned: {t.get('assigned_to') or 'Unassigned'}")

def view_summary(tickets):
    print_header("CampusFlow Operational Summary")
    summary = get_summary(tickets)
    print(f"Total Tickets Tracked: {summary['total']}")
    print("\nBy Status:")
    for status, count in summary['by_status'].items():
        print(f"  - {status.replace('_', ' ').capitalize()}: {count}")
    print("\nBy Priority:")
    for priority, count in summary['by_priority'].items():
        print(f"  - {priority.capitalize()}: {count}")

def handle_create(tickets):
    print_header("Create New Support Ticket")
    title = input("Enter problem title: ")
    
    print(f"Allowed Categories: {', '.join(ALLOWED_CATEGORIES)}")
    category = input("Enter category: ")
    
    print(f"Allowed Urgencies: {', '.join(ALLOWED_URGENCIES)}")
    urgency = input("Enter urgency: ")
    
    affected = input("Enter number of affected users: ")

    res = create_ticket(tickets, title, category, urgency, affected)
    if res["success"]:
        print(f"\n✅ Ticket successfully created! Generated ID: {res['ticket']['id']} [Priority: {res['ticket']['priority']}]")
        save_tickets(DB_FILE, tickets)
    else:
        print(f"\n❌ Error: {res['error']}")

def handle_assign(tickets):
    print_header("Assign Ticket to Staff")
    t_id = input("Enter Ticket ID: ")
    name = input("Enter staff name: ")
    try:
        assign(tickets, t_id, name)
        print(f"\n✅ Ticket {t_id} successfully assigned to {name}.")
        save_tickets(DB_FILE, tickets)
    except ValueError as e:
        print(f"\n❌ Workflow Error: {e}")

def handle_status(tickets):
    print_header("Update Ticket Status")
    t_id = input("Enter Ticket ID: ")
    new_status = input("Enter new status (in_progress / resolved): ")
    try:
        change_status(tickets, t_id, new_status)
        print(f"\n✅ Ticket {t_id} successfully updated to '{new_status}'.")
        save_tickets(DB_FILE, tickets)
    except ValueError as e:
        print(f"\n❌ Workflow Error: {e}")

def handle_reopen(tickets):
    print_header("Reopen Resolved Ticket")
    t_id = input("Enter Ticket ID: ")
    try:
        reopen(tickets, t_id)
        print(f"\n✅ Ticket {t_id} successfully reopened to 'open'.")
        save_tickets(DB_FILE, tickets)
    except ValueError as e:
        print(f"\n❌ Workflow Error: {e}")

def main():
    try:
        tickets = load_tickets(DB_FILE)
    except StorageError as e:
        print(f"Critical Database Error: {e}")
        tickets = []

    while True:
        print("\n==============================")
        print("   CAMPUSFLOW HELP DESK APP   ")
        print("==============================")
        print("1. View Priority Work Queue")
        print("2. Create a Ticket")
        print("3. Assign a Ticket")
        print("4. Update Ticket Status")
        print("5. Reopen a Ticket")
        print("6. View System Summary Dashboard")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == "1":
            view_queue(tickets)
        elif choice == "2":
            handle_create(tickets)
        elif choice == "3":
            handle_assign(tickets)
        elif choice == "4":
            handle_status(tickets)
        elif choice == "5":
            handle_reopen(tickets)
        elif choice == "6":
            view_summary(tickets)
        elif choice == "7":
            print("\nSaving database... Goodbye!")
            save_tickets(DB_FILE, tickets)
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please choose between 1 and 7.")

if __name__ == "__main__":
    main()
