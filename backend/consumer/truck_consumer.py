import json
from confluent_kafka import Consumer
import state_store

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'truck-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

consumer.subscribe(['truck-events'])
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

        truck_id = event["truck_id"]
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
            state_store.record_reading(truck_id, temperature)
        

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
    