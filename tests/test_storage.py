import unittest
import json
from pathlib import Path
from campusflow.storage import load_tickets, save_tickets, StorageError

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = Path("test_tickets_db.json")
        self.sample_data = [{"id": "T001", "title": "Wi-Fi Issue", "status": "open"}]

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
        self.test_file.write_text(json.dumps([{"id": "invalid"}]))
        with self.assertRaises(StorageError):
            load_tickets(self.test_file)

    def test_duplicate_ticket_ids_raise_without_replacing_memory(self):
        self.test_file.write_text(json.dumps([{"id": "T001"}, {"id": "t001"}]))
        tickets = [{"id": "T009", "title": "Keep this ticket"}]

        with self.assertRaises(StorageError):
            tickets[:] = load_tickets(self.test_file)

        self.assertEqual(tickets, [{"id": "T009", "title": "Keep this ticket"}])

if __name__ == "__main__":
    unittest.main()
