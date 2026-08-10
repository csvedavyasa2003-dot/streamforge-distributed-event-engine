import json
from datetime import datetime, timezone
from collections import defaultdict

import requests
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'truck-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['truck-events'])

API_URL = "http://localhost:8000/events/"
WINDOW_SECONDS = 300  # 5 minutes

# windows[truck_id][window_start_epoch] = list of temperatures
windows = defaultdict(lambda: defaultdict(list))
# tracks which windows have already been flushed, so we don't save twice
flushed_windows = set()


def get_window_start(timestamp_str):
    """Round an ISO timestamp down to the nearest 5-minute boundary."""
    dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    epoch = int(dt.timestamp())
    window_start = epoch - (epoch % WINDOW_SECONDS)
    return window_start


def flush_window(truck_id, window_start, temps):
    """Save a completed window's average temperature to the database."""
    key = (truck_id, window_start)
    if key in flushed_windows:
        return
    flushed_windows.add(key)

    avg_temp = sum(temps) / len(temps)
    window_time = datetime.fromtimestamp(window_start, tz=timezone.utc).isoformat()

    print(f"\n📊 WINDOW CLOSED — Truck {truck_id}")
    print(f"   Window start : {window_time}")
    print(f"   Events       : {len(temps)}")
    print(f"   Avg temp     : {avg_temp:.2f}°C")

    payload = {
        "truck_id": str(truck_id),
        "temperature": round(avg_temp, 2),
        "humidity": 0,
        "speed": 0,
        "gps_location": "windowed-aggregate",
        "fuel_level": 0,
        "timestamp": window_time,
    }

    try:
        requests.post(API_URL, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        print("Failed to save windowed result:", e)


print("Listening for truck events (windowed mode)... Press Ctrl+C to stop.")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer Error:", msg.error())
            continue

        event = json.loads(msg.value().decode("utf-8"))
        truck_id = event["truck_id"]
        temperature = event["temperature"]
        timestamp = event["timestamp"]

        window_start = get_window_start(timestamp)
        windows[truck_id][window_start].append(temperature)

        # Check if any of this truck's older windows are now "complete"
        # (i.e., we've moved past them based on the latest event's timestamp)
        current_window = window_start
        for w_start in list(windows[truck_id].keys()):
            if w_start < current_window:
                flush_window(truck_id, w_start, windows[truck_id][w_start])

        print(f"Truck {truck_id} | Temp {temperature}°C | Window {window_start} | "
              f"Events in current window: {len(windows[truck_id][window_start])}")

except KeyboardInterrupt:
    print("\nConsumer stopped. Flushing remaining windows...")
    for truck_id, truck_windows in windows.items():
        for w_start, temps in truck_windows.items():
            flush_window(truck_id, w_start, temps)

finally:
    consumer.close()