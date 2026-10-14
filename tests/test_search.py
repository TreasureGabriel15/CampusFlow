import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T1", "title": "Wifi down in library", "category": "network", "status": "open", "priority": "high"},
            {"id": "T2", "title": "Projector broken", "category": "hardware", "status": "in_progress", "priority": "medium"},
            {"id": "T3", "title": "WIFI slow in dorm", "category": "network", "status": "resolved", "priority": "low"},
            {"id": "T4", "title": "Printer jam", "category": "hardware", "status": "open", "priority": "critical"},
        ]

    def ids(self, results):
        return [t["id"] for t in results]

    def test_no_filters_returns_all(self):
        self.assertEqual(self.ids(search_tickets(self.tickets)), ["T1", "T2", "T3", "T4"])

    def test_title_match_is_case_insensitive(self):
        self.assertEqual(self.ids(search_tickets(self.tickets, title="wifi")), ["T1", "T3"])

    def test_title_partial_match(self):
        self.assertEqual(self.ids(search_tickets(self.tickets, title="proj")), ["T2"])

    def test_blank_or_whitespace_title_returns_all(self):
        self.assertEqual(len(search_tickets(self.tickets, title="   ")), 4)

    def test_filter_by_category(self):
        self.assertEqual(self.ids(search_tickets(self.tickets, category="hardware")), ["T2", "T4"])

    def test_filter_by_status(self):
        self.assertEqual(self.ids(search_tickets(self.tickets, status="open")), ["T1", "T4"])

    def test_filter_by_priority(self):
        self.assertEqual(self.ids(search_tickets(self.tickets, priority="low")), ["T3"])

    def test_filters_are_case_insensitive(self):
        result = search_tickets(self.tickets, category="NETWORK", status="Open")
        self.assertEqual(self.ids(result), ["T1"])