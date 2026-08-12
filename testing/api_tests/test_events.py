import unittest
import json
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


class TestEventAPI(unittest.TestCase):

    def test_home(self):
        response = urlopen(f"{BASE_URL}/")
        self.assertEqual(response.status, 200)

    def test_get_events(self):
        response = urlopen(f"{BASE_URL}/events/")
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)

    def test_create_event(self):
        event = {
            "truck_id": "TEST-AUTOMATED-001",
            "temperature": 30.5,
            "humidity": 60,
            "speed": 70,
            "gps_location": "12.9716,77.5946",
            "fuel_level": 75,
            "timestamp": "2026-08-12T11:00:00"
        }

        request = Request(
            f"{BASE_URL}/events/",
            data=json.dumps(event).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        response = urlopen(request)

        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())

        self.assertEqual(data["truck_id"], "TEST-AUTOMATED-001")
        self.assertEqual(data["temperature"], 30.5)

    def test_statistics(self):
        response = urlopen(f"{BASE_URL}/events/stats")
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())

        self.assertIn("total_events", data)
        self.assertIn("average_temperature", data)
        self.assertIn("highest_temperature", data)
        self.assertIn("lowest_temperature", data)

    def test_alerts(self):
        response = urlopen(f"{BASE_URL}/events/alerts")
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)

    def test_workers(self):
        response = urlopen(f"{BASE_URL}/events/workers")
        self.assertEqual(response.status, 200)

        data = json.loads(response.read().decode())
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()