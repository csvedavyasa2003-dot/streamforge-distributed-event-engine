import unittest
import json
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


class TestEventIntegration(unittest.TestCase):

    def test_event_create_and_retrieve_flow(self):
        event = {
            "truck_id": "INTEGRATION-001",
            "temperature": 28.5,
            "humidity": 60,
            "speed": 65,
            "gps_location": "12.9716,77.5946",
            "fuel_level": 75,
            "timestamp": "2026-08-12T12:30:00"
        }

        # Step 1: Create event
        request = Request(
            f"{BASE_URL}/events/",
            data=json.dumps(event).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        response = urlopen(request)

        self.assertEqual(response.status, 200)

        created_event = json.loads(
            response.read().decode("utf-8")
        )

        self.assertEqual(
            created_event["truck_id"],
            "INTEGRATION-001"
        )

        # Step 2: Retrieve events
        response = urlopen(f"{BASE_URL}/events/")

        self.assertEqual(response.status, 200)

        events = json.loads(
            response.read().decode("utf-8")
        )

        # Step 3: Verify event exists in database
        matching_events = [
            event for event in events
            if event["truck_id"] == "INTEGRATION-001"
        ]

        self.assertTrue(len(matching_events) > 0)

        saved_event = matching_events[0]

        self.assertEqual(
            saved_event["temperature"],
            28.5
        )

        self.assertEqual(
            saved_event["fuel_level"],
            75
        )


if __name__ == "__main__":
    unittest.main()