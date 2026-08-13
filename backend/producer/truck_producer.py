import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def generate_truck_event(truck_id):
    return {
        "truck_id": truck_id,
        "temperature": round(random.uniform(15, 40), 1),
        "humidity": round(random.uniform(30, 90), 1),
        "speed": round(random.uniform(0, 120), 1),
        "gps_location": {
            "lat": round(random.uniform(-90, 90), 4),
            "lon": round(random.uniform(-180, 180), 4)
        },
        "fuel_level": round(random.uniform(0, 100), 1),
        "timestamp": datetime.utcnow().isoformat()
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Sent: {msg.value().decode('utf-8')[:80]}...")

if __name__ == "__main__":
    num_trucks = 10
    print("Starting truck event producer... Press Ctrl+C to stop.")
    try:
        while True:
            for truck_id in range(1001, 1001 + num_trucks):
                event = generate_truck_event(truck_id)
                producer.produce(
                    "truck-events",
                    value=json.dumps(event).encode("utf-8"),
                    callback=delivery_report
                )
            producer.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")