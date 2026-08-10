# Kafka Setup Notes

## Topic Configuration

The `truck-events` topic is configured with **8 partitions** to support
parallel consumer processing and demonstrate real multi-worker behavior.

If setting up this project fresh (new environment, new Kafka container),
run this once to configure the topic correctly:

```bash
docker exec -it streamforge-distributed-event-engine-kafka-1 kafka-topics --alter --topic truck-events --partitions 8 --bootstrap-server localhost:9092
```

To verify the partition count:

```bash
docker exec -it streamforge-distributed-event-engine-kafka-1 kafka-topics --describe --topic truck-events --bootstrap-server localhost:9092
```

## Running Multiple Consumer Workers

`consumer/truck_consumer.py` uses a shared consumer group
(`group.id: 'truck-consumer-group'`). This means multiple instances of the
script can be run simultaneously, and Kafka will automatically distribute
the 8 partitions across however many consumer processes are active.

To simulate multiple parallel workers, open separate terminals and run:

```bash
cd backend
.\venv\Scripts\Activate.ps1
python consumer/truck_consumer.py
```

...once per worker (e.g., run this in 2-4 separate terminals).

## Verifying Partition Assignment

To see which consumer instance owns which partitions, run:

```bash
docker exec -it streamforge-distributed-event-engine-kafka-1 kafka-consumer-groups --describe --group truck-consumer-group --bootstrap-server localhost:9092
```

This shows a live table of `PARTITION`, `CONSUMER-ID`, and `HOST`, proving
that Kafka is genuinely load-balancing across multiple worker processes.

## Chaos Testing (Partition Rebalancing)

With 2+ consumers running, stopping one (`Ctrl+C`) triggers Kafka's native
consumer group rebalancing protocol — the surviving consumer(s) will
automatically be reassigned the partitions previously owned by the stopped
one, with no manual intervention required. This demonstrates the
fault-tolerance behavior described in the project specification, using
Kafka's built-in rebalancing rather than a custom implementation.