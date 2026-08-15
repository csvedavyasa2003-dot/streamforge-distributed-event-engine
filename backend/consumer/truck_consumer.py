import json
import time
import uuid
import threading
from datetime import datetime, timezone
from collections import defaultdict

import requests
from confluent_kafka import Consumer
from rocksdict import Rdict
from prometheus_client import start_http_server, Counter, Gauge

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'truck-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['truck-events'])

API_URL = "http://localhost:8000/events/"
WINDOW_SECONDS = 300  # 5 minutes

# --- Worker heartbeat setup ---
WORKER_ID = f"worker-{uuid.uuid4().hex[:8]}"
HEARTBEAT_URL = "http://localhost:8000/events/workers/heartbeat"
HEARTBEAT_INTERVAL = 5  # seconds


def send_heartbeats():
    while True:
        try:
            requests.post(HEARTBEAT_URL, params={"worker_id": WORKER_ID}, timeout=2)
        except requests.exceptions.RequestException:
            pass
        time.sleep(HEARTBEAT_INTERVAL)


heartbeat_thread = threading.Thread(target=send_heartbeats, daemon=True)
heartbeat_thread.start()

print(f"Worker ID: {WORKER_ID}")

# --- Prometheus metrics ---
events_processed_total = Counter(
    'truck_events_processed_total', 'Total events processed', ['worker_id']
)
current_window_size = Gauge(
    'truck_window_size', 'Number of events in current window', ['truck_id']
)
processing_lag_seconds = Gauge(
    'truck_processing_lag_seconds', 'Time between event timestamp and processing', ['worker_id']
)

METRICS_PORT = 8100
start_http_server(METRICS_PORT)
print(f"Prometheus metrics available at http://localhost:{METRICS_PORT}/metrics")

# --- RocksDB state store — persists window data to disk, survives restarts ---
db = Rdict("rocksdb_state")
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

    del db[key]


print(f"Listening for truck events (windowed mode, RocksDB-backed)... Worker: {WORKER_ID}")
print("Press Ctrl+C to stop.")

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

        # --- 1. Windowed aggregation (RocksDB-backed) ---
        window_start = get_window_start(timestamp)
        temps = add_event_to_window(truck_id, window_start, temperature)

        for w_start in get_windows_for_truck(truck_id):
            if w_start < window_start:
                flush_window(truck_id, w_start)

        # --- 2. Also save the raw event immediately, so dashboard stats stay live ---
        raw_payload = {
            "truck_id": str(truck_id),
            "temperature": temperature,
            "humidity": event.get("humidity", 0),
            "speed": event.get("speed", 0),
            "gps_location": json.dumps(event.get("gps_location", {})),
            "fuel_level": event.get("fuel_level", 0),
            "timestamp": timestamp,
        }
        try:
            requests.post(API_URL, json=raw_payload, timeout=2)
        except requests.exceptions.RequestException as e:
            print("Failed to save raw event to API:", e)

        # --- 3. Record Prometheus metrics ---
        events_processed_total.labels(worker_id=WORKER_ID).inc()
        current_window_size.labels(truck_id=truck_id).set(len(temps))

        event_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)
        lag = (datetime.now(timezone.utc) - event_time).total_seconds()
        processing_lag_seconds.labels(worker_id=WORKER_ID).set(lag)

        print(f"Truck {truck_id} | Temp {temperature}°C | Window {window_start} | "
              f"Events in current window: {len(temps)} (RocksDB) | Worker: {WORKER_ID}")

except KeyboardInterrupt:
    print("\nConsumer stopped. Flushing remaining windows...")
    for key in list(db.keys()):
        truck_id, window_start = key.split(":")
        flush_window(truck_id, int(window_start))

finally:
    consumer.close()
    db.close()
    flushed_db.close()