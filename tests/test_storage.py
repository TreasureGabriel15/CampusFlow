import unittest
import json
from pathlib import Path
from campusflow.storage import load_tickets, save_tickets, StorageError
from campusflow.notes import add_note
from campusflow.tickets import create_ticket, next_ticket_id


def make_ticket(ticket_id="T001"):
    return {
        "id": ticket_id,
        "title": "Wi-Fi Issue",
        "category": "Network",
        "urgency": "high",
        "affected_users": 15,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = Path("test_tickets_db.json")
        self.sample_data = [make_ticket()]

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_save_and_load_tickets_matches(self):
        save_tickets(self.test_file, self.sample_data)
        loaded = load_tickets(self.test_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "T001")

    def test_load_non_existent_file_returns_empty_list(self):
        loaded = load_tickets("missing_file_xyz.json")
        self.assertEqual(loaded, [])

    def test_corrupt_json_raises_storage_error(self):
        self.test_file.write_text("invalid-json-content-here")
        with self.assertRaises(StorageError):
            load_tickets(self.test_file)

    def test_non_object_ticket_raises_storage_error(self):
        self.test_file.write_text(json.dumps([None]))
        with self.assertRaises(StorageError):
            load_tickets(self.test_file)

    def test_invalid_ticket_id_raises_storage_error(self):
        ticket = make_ticket("invalid")
        self.test_file.write_text(json.dumps([ticket]))
        with self.assertRaises(StorageError):
            load_tickets(self.test_file)

    def test_duplicate_ticket_ids_raise_without_replacing_memory(self):
        self.test_file.write_text(json.dumps([make_ticket(), make_ticket("t001")]))
        tickets = [make_ticket("T009")]

        with self.assertRaises(StorageError):
            tickets[:] = load_tickets(self.test_file)

        self.assertEqual(tickets, [make_ticket("T009")])

    def test_invalid_ticket_fields_raise_storage_error(self):
        invalid_cases = (
            ("missing title", lambda ticket: ticket.pop("title")),
            ("blank title", lambda ticket: ticket.update(title="  ")),
            ("invalid category", lambda ticket: ticket.update(category="Otherish")),
            ("invalid urgency", lambda ticket: ticket.update(urgency="urgent")),
            ("invalid affected users", lambda ticket: ticket.update(affected_users=True)),
            ("inconsistent priority", lambda ticket: ticket.update(priority="low")),
            ("invalid status", lambda ticket: ticket.update(status="closed")),
            ("invalid assignee", lambda ticket: ticket.update(assigned_to="  ")),
        )
        for label, invalidate in invalid_cases:
            with self.subTest(label=label):
                ticket = make_ticket()
                invalidate(ticket)
                self.test_file.write_text(json.dumps([ticket]))
                with self.assertRaises(StorageError):
                    load_tickets(self.test_file)

    def test_invalid_note_and_duplicate_note_ids_raise_storage_error(self):
        invalid_notes = (
            [{"note_id": "bad", "author": "Alice", "message": "Good update"}],
            [
                {"note_id": "N001", "author": "Alice", "message": "First update"},
                {"note_id": "n001", "author": "Bob", "message": "Second update"},
            ],
            [{"note_id": "N001", "author": " ", "message": "Good update"}],
            [{"note_id": "N001", "author": "Alice", "message": "Tiny"}],
        )
        for notes in invalid_notes:
            with self.subTest(notes=notes):
                ticket = make_ticket()
                ticket["notes"] = notes
                self.test_file.write_text(json.dumps([ticket]))
                with self.assertRaises(StorageError):
                    load_tickets(self.test_file)

    def test_legacy_ticket_without_notes_loads_with_empty_notes(self):
        ticket = make_ticket()
        del ticket["notes"]
        self.test_file.write_text(json.dumps([ticket]))

        loaded = load_tickets(self.test_file)

        self.assertEqual(loaded[0]["notes"], [])
        self.assertNotIn("notes", ticket)

    def test_reload_preserves_notes_and_next_ticket_and_note_ids(self):
        ticket = make_ticket("T009")
        tickets = [ticket]
        first_note = add_note(tickets, "T009", "Alice", "First update")
        self.assertEqual(first_note["note_id"], "N001")
        save_tickets(self.test_file, tickets)

        reloaded = load_tickets(self.test_file)

        self.assertEqual(reloaded, tickets)
        self.assertEqual(next_ticket_id(reloaded), "T010")
        second_note = add_note(reloaded, "T009", "Bob", "Second update")
        self.assertEqual(second_note["note_id"], "N002")
        result = create_ticket(reloaded, "Printer issue", "hardware", "low", 1)
        self.assertTrue(result["success"])
        self.assertEqual(result["ticket"]["id"], "T010")

if __name__ == "__main__":
    unittest.main()
