import unittest

from campusflow.reports import get_summary, get_work_queue


def make(ticket_id, priority="medium", status="open"):
    return {"id": ticket_id, "priority": priority, "status": status}


def ids(rows):
    return [t["id"] for t in rows]


class TestGetWorkQueue(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(get_work_queue([]), [])

    def test_resolved_tickets_are_excluded(self):
        tickets = [make("T1", status="resolved"), make("T2", status="open")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T2"])

    def test_open_and_in_progress_are_included(self):
        tickets = [make("T1", status="open"), make("T2", status="in_progress")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T1", "T2"])

    def test_all_resolved_returns_empty(self):
        tickets = [make("T1", status="resolved"), make("T2", status="resolved")]
        self.assertEqual(get_work_queue(tickets), [])

    def test_sorted_by_priority(self):
        tickets = [
            make("T1", "low"),
            make("T2", "critical"),
            make("T3", "medium"),
            make("T4", "high"),
        ]
        self.assertEqual(ids(get_work_queue(tickets)), ["T2", "T4", "T3", "T1"])

    def test_same_priority_sorted_by_ticket_number(self):
        tickets = [make("T10", "high"), make("T2", "high"), make("T1", "high")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T1", "T2", "T10"])

    def test_number_sort_is_numeric_not_alphabetical(self):
        tickets = [make("T100"), make("T20"), make("T3")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T3", "T20", "T100"])

    def test_leading_zeros_in_ids(self):
        tickets = [make("T010"), make("T002")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T002", "T010"])

    def test_unknown_priority_goes_last(self):
        tickets = [make("T1", "urgent"), make("T2", "low")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T2", "T1"])

    def test_missing_priority_goes_last(self):
        tickets = [{"id": "T1", "status": "open"}, make("T2", "low")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T2", "T1"])

    def test_id_without_digits_sorts_after_numbered_ids(self):
        tickets = [make("ABC", "high"), make("T5", "high")]
        self.assertEqual(ids(get_work_queue(tickets)), ["T5", "ABC"])

    def test_missing_id_does_not_crash(self):
        tickets = [{"priority": "high", "status": "open"}, make("T1", "high")]
        self.assertEqual(len(get_work_queue(tickets)), 2)

    def test_missing_status_counts_as_waiting(self):
        tickets = [{"id": "T1", "priority": "high"}]
        self.assertEqual(ids(get_work_queue(tickets)), ["T1"])

    def test_does_not_modify_input(self):
        tickets = [make("T2", "low"), make("T1", "critical")]
        before = [dict(t) for t in tickets]
        get_work_queue(tickets)
        self.assertEqual(tickets, before)
        self.assertEqual(ids(tickets), ["T2", "T1"])


class TestGetSummary(unittest.TestCase):
    def test_empty_list(self):
        result = get_summary([])
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["by_status"], {"open": 0, "in_progress": 0, "resolved": 0})
        self.assertEqual(result["by_priority"], {"critical": 0, "high": 0, "medium": 0, "low": 0})

    def test_total_counts_all_tickets(self):
        tickets = [make("T1"), make("T2"), make("T3", status="resolved")]
        self.assertEqual(get_summary(tickets)["total"], 3)

    def test_counts_by_status(self):
        tickets = [
            make("T1", status="open"),
            make("T2", status="open"),
            make("T3", status="in_progress"),
            make("T4", status="resolved"),
        ]
        self.assertEqual(
            get_summary(tickets)["by_status"],
            {"open": 2, "in_progress": 1, "resolved": 1},
        )

    def test_counts_by_priority(self):
        tickets = [
            make("T1", "critical"),
            make("T2", "high"),
            make("T3", "high"),
            make("T4", "low"),
        ]
        self.assertEqual(
            get_summary(tickets)["by_priority"],
            {"critical": 1, "high": 2, "medium": 0, "low": 1},
        )

    def test_unknown_values_are_not_counted_but_still_in_total(self):
        tickets = [make("T1", "urgent", "pending"), make("T2", "low", "open")]
        result = get_summary(tickets)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["by_status"], {"open": 1, "in_progress": 0, "resolved": 0})
        self.assertEqual(result["by_priority"], {"critical": 0, "high": 0, "medium": 0, "low": 1})

    def test_missing_fields_do_not_crash(self):
        result = get_summary([{"id": "T1"}])
        self.assertEqual(result["total"], 1)
        self.assertEqual(sum(result["by_status"].values()), 0)
        self.assertEqual(sum(result["by_priority"].values()), 0)

    def test_does_not_modify_input(self):
        tickets = [make("T1", "high", "open")]
        before = [dict(t) for t in tickets]
        get_summary(tickets)
        self.assertEqual(tickets, before)


if __name__ == "__main__":
    unittest.main()