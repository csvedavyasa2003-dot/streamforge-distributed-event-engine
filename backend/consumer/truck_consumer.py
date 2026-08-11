import json
from datetime import datetime, timezone
from collections import defaultdict

import requests
from confluent_kafka import Consumer
from rocksdict import Rdict

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'truck-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['truck-events'])

API_URL = "http://localhost:8000/events/"
WINDOW_SECONDS = 300  # 5 minutes

# RocksDB state store — persists window data to disk, survives restarts
db = Rdict("rocksdb_state")

# Tracks which windows have already been flushed (also persisted)
flushed_db = Rdict("rocksdb_flushed")


def get_window_start(timestamp_str):
    dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    epoch = int(dt.timestamp())
    return epoch - (epoch % WINDOW_SECONDS)


def make_key(truck_id, window_start):
    return f"{truck_id}:{window_start}"


def add_event_to_window(truck_id, window_start, temperature):
    key = make_key(truck_id, window_start)
    temps = db.get(key, [])
    temps.append(temperature)
    db[key] = temps
    return temps


def get_windows_for_truck(truck_id):
    """Returns all window_start values currently stored for a given truck."""
    prefix = f"{truck_id}:"
    result = []
    for key in db.keys():
        if key.startswith(prefix):
            window_start = int(key.split(":")[1])
            result.append(window_start)
    return result


def flush_window(truck_id, window_start):
    key = make_key(truck_id, window_start)

    if flushed_db.get(key):
        return

    temps = db.get(key)
    if not temps:
        return

    flushed_db[key] = True

    avg_temp = sum(temps) / len(temps)
    window_time = datetime.fromtimestamp(window_start, tz=timezone.utc).isoformat()

    print(f"\n📊 WINDOW CLOSED — Truck {truck_id}")
    print(f"   Window start : {window_time}")
    print(f"   Events       : {len(temps)}")
    print(f"   Avg temp     : {avg_temp:.2f}°C")
    print(f"   (persisted via RocksDB)")

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

    # Clean up the flushed window's raw data from the state store
    del db[key]


print("Listening for truck events (windowed mode, RocksDB-backed)... Press Ctrl+C to stop.")

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
        temps = add_event_to_window(truck_id, window_start, temperature)

        # Flush any older windows for this truck that we've now moved past
        for w_start in get_windows_for_truck(truck_id):
            if w_start < window_start:
                flush_window(truck_id, w_start)

        print(f"Truck {truck_id} | Temp {temperature}°C | Window {window_start} | "
              f"Events in current window: {len(temps)} (RocksDB)")

except KeyboardInterrupt:
    print("\nConsumer stopped. Flushing remaining windows...")
    for key in list(db.keys()):
        truck_id, window_start = key.split(":")
        flush_window(truck_id, int(window_start))

finally:
    consumer.close()
    db.close()
    flushed_db.close()