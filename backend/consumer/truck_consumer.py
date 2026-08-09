import json
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

# Worker state
total_events = 0
total_temperature = 0

highest_temperature = float("-inf")
lowest_temperature = float("inf")

alert_count = 0


print("Listening for truck events... Press Ctrl+C to stop.")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer Error:", msg.error())
            continue

        event = json.loads(msg.value().decode("utf-8"))

        temperature = event["temperature"]

        total_events += 1
        total_temperature += temperature

        if temperature > highest_temperature:
            highest_temperature = temperature

        if temperature < lowest_temperature:
            lowest_temperature = temperature

        average_temperature = total_temperature / total_events

        if temperature > 35:
            alert_count += 1

            print("\n🚨 HIGH TEMPERATURE ALERT!")
            print(f"Truck ID    : {event['truck_id']}")
            print(f"Temperature : {temperature} °C")

        # Save event to the database via FastAPI
        payload = {
            "truck_id": str(event["truck_id"]),
            "temperature": event["temperature"],
            "humidity": event["humidity"],
            "speed": event["speed"],
            "gps_location": json.dumps(event["gps_location"]),
            "fuel_level": event["fuel_level"],
            "timestamp": event["timestamp"],
        }

        try:
            requests.post(API_URL, json=payload, timeout=2)
        except requests.exceptions.RequestException as e:
            print("Failed to save event to API:", e)

        print("\nReceived Event")
        print(f"Truck ID     : {event['truck_id']}")
        print(f"Temperature  : {event['temperature']} °C")
        print(f"Humidity     : {event['humidity']} %")
        print(f"Speed        : {event['speed']} km/h")
        print(f"Fuel Level   : {event['fuel_level']} %")
        print(f"GPS          : {event['gps_location']}")
        print(f"Timestamp    : {event['timestamp']}")


        print("\n----- Worker Statistics -----")
        print(f"Total Events        : {total_events}")
        print(f"Average Temperature : {average_temperature:.2f} °C")
        print(f"Highest Temperature : {highest_temperature} °C")
        print(f"Lowest Temperature  : {lowest_temperature} °C")
        print(f"High Temp Alerts    : {alert_count}")
        print("-----------------------------")

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()