import unittest
from campusflow.workflow import assign, change_status, reopen

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T001", "status": "open", "assigned_to": ""},
            {"id": "T002", "status": "in_progress", "assigned_to": "Alice"},
            {"id": "T003", "status": "resolved", "assigned_to": "Bob"}
        ]

    def test_assign_staff_successfully(self):
        ticket = assign(self.tickets, "T001", "Charlie")
        self.assertEqual(ticket["assigned_to"], "Charlie")

    def test_assign_blank_name_raises_error(self):
        with self.assertRaises(ValueError):
            assign(self.tickets, "T001", "   ")

    def test_change_status_valid_progression(self):
        ticket = change_status(self.tickets, "T002", "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_cannot_skip_status_progression(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")

    def test_unassigned_in_progress_raises_error(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

    def test_reopen_resolved_ticket(self):
        ticket = reopen(self.tickets, "T003")
        self.assertEqual(ticket["status"], "open")

    def test_cannot_reopen_active_ticket(self):
        with self.assertRaises(ValueError):
            reopen(self.tickets, "T001")

if __name__ == "__main__":
    unittest.main()
