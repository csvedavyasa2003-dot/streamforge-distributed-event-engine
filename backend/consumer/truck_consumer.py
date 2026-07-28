import json
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'truck-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

consumer.subscribe(['truck-events'])

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

        print("\nReceived Event")
        print(f"Truck ID     : {event['truck_id']}")
        print(f"Temperature  : {event['temperature']} °C")
        print(f"Humidity     : {event['humidity']} %")
        print(f"Speed        : {event['speed']} km/h")
        print(f"Fuel Level   : {event['fuel_level']} %")
        print(f"GPS          : {event['gps_location']}")
        print(f"Timestamp    : {event['timestamp']}")

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()