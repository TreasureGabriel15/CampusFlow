import unittest
from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    find_ticket,
    next_ticket_id,
)


class TestPriority(unittest.TestCase):

    def test_high_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_and_exactly_ten_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_and_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_and_many_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_and_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_medium_and_one_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")


class TestCreateTicket(unittest.TestCase):

    def test_create_valid_ticket(self):
        tickets = []
        result = create_ticket(tickets, "Wi-Fi down", "network", "HIGH", "15")
        self.assertTrue(result["success"])
        t = result["ticket"]
        self.assertEqual(t["id"], "T001")
        self.assertEqual(t["category"], "Network")
        self.assertEqual(t["urgency"], "high")
        self.assertEqual(t["priority"], "critical")
        self.assertEqual(t["status"], "open")
        self.assertIsNone(t["assigned_to"])
        self.assertEqual(len(tickets), 1)

    def test_blank_title_rejected(self):
        result = create_ticket([], "   ", "network", "high", "5")
        self.assertFalse(result["success"])

    def test_invalid_category_rejected(self):
        result = create_ticket([], "X", "banana", "high", "5")
        self.assertFalse(result["success"])

    def test_invalid_urgency_rejected(self):
        result = create_ticket([], "X", "network", "urgent", "5")
        self.assertFalse(result["success"])

    def test_zero_users_rejected(self):
        result = create_ticket([], "X", "network", "high", "0")
        self.assertFalse(result["success"])

    def test_negative_users_rejected(self):
        result = create_ticket([], "X", "network", "high", "-3")
        self.assertFalse(result["success"])

    def test_non_numeric_users_rejected(self):
        result = create_ticket([], "X", "network", "high", "abc")
        self.assertFalse(result["success"])

    def test_decimal_users_rejected(self):
        result = create_ticket([], "X", "network", "high", "3.5")
        self.assertFalse(result["success"])

    def test_ids_increment(self):
        tickets = []
        create_ticket(tickets, "A", "network", "high", "1")
        create_ticket(tickets, "B", "network", "high", "1")
        self.assertEqual(tickets[0]["id"], "T001")
        self.assertEqual(tickets[1]["id"], "T002")


class TestFindTicket(unittest.TestCase):

    def test_find_existing(self):
        tickets = [{"id": "T001", "title": "A"}, {"id": "T002", "title": "B"}]
        found = find_ticket(tickets, "T002")
        self.assertIsNotNone(found)
        self.assertEqual(found["title"], "B")

    def test_find_missing_returns_none(self):
        self.assertIsNone(find_ticket([], "T999"))


class TestNextId(unittest.TestCase):

    def test_first_id_is_t001(self):
        self.assertEqual(next_ticket_id([]), "T001")

    def test_id_increments(self):
        tickets = [{"id": "T001"}, {"id": "T002"}]
        self.assertEqual(next_ticket_id(tickets), "T003")

    def test_id_uses_max(self):
        tickets = [{"id": "T001"}, {"id": "T009"}]
        self.assertEqual(next_ticket_id(tickets), "T010")


if __name__ == "__main__":
    unittest.main()