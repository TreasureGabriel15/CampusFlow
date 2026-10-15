import copy
import unittest

from campusflow.notes import add_note
from campusflow.workflow import assign, change_status, reopen


class TestAddNote(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T001", "status": "open"},
            {"id": "T002", "status": "in_progress", "notes": []},
            {"id": "T003", "status": "resolved", "notes": []},
        ]

    def test_add_note_to_open_ticket(self):
        note = add_note(self.tickets, "t001", "  Alice  ", "  Wi-Fi is back.  ")
        self.assertEqual(
            note,
            {"note_id": "N001", "author": "Alice", "message": "Wi-Fi is back."},
        )
        self.assertEqual(self.tickets[0]["notes"], [note])

    def test_note_ids_increment_independently_per_ticket(self):
        first = add_note(self.tickets, "T001", "Alice", "First")
        second = add_note(self.tickets, "T002", "Bob", "Second")
        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N001")

    def test_note_id_increments_for_same_ticket(self):
        first = add_note(self.tickets, "T001", "Alice", "First")
        second = add_note(self.tickets, "T001", "Bob", "Second")
        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_notes_survive_resolution_and_reopening(self):
        assign(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        first_note = add_note(self.tickets, "T001", "Alice", "First update")
        change_status(self.tickets, "T001", "resolved")
        resolved_notes = copy.deepcopy(self.tickets[0]["notes"])

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Bob", "Follow-up update")
        self.assertEqual(self.tickets[0]["notes"], resolved_notes)

        reopen(self.tickets, "T001")
        second_note = add_note(self.tickets, "T001", "Bob", "Follow-up update")

        self.assertEqual(self.tickets[0]["notes"], [first_note, second_note])
        self.assertEqual([note["note_id"] for note in self.tickets[0]["notes"]], ["N001", "N002"])

    def test_reject_note_on_resolved_ticket_without_mutation(self):
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T003", "Alice", "Follow-up")
        self.assertEqual(self.tickets, before)

    def test_reject_blank_author_without_mutation(self):
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", " ", "Message")
        self.assertEqual(self.tickets, before)

    def test_reject_blank_message_without_mutation(self):
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", " ")
        self.assertEqual(self.tickets, before)

    def test_reject_short_message_without_consuming_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", "Four")
        note = add_note(self.tickets, "T001", "Alice", "Valid")
        self.assertEqual(note["note_id"], "N001")

    def test_reject_long_message_without_consuming_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Alice", "x" * 301)
        note = add_note(self.tickets, "T001", "Alice", "Valid")
        self.assertEqual(note["note_id"], "N001")

    def test_accept_message_at_300_character_limit(self):
        note = add_note(self.tickets, "T001", "Alice", "x" * 300)
        self.assertEqual(len(note["message"]), 300)

    def test_reject_unknown_ticket_without_mutation(self):
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Alice", "Message")
        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()
