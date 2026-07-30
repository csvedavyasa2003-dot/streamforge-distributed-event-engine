# StreamForge Architecture

## Project Overview

StreamForge is a distributed event processing engine that simulates real-time event streaming. It receives events, distributes them using Apache Kafka, processes them through worker services, stores processed data, exposes REST APIs using FastAPI, and visualizes information through a React dashboard.

---

# Objectives

- Process real-time events
- Build scalable architecture
- Support multiple workers
- Monitor system performance
- Demonstrate distributed computing

---

# High-Level Architecture

Event Generator
        │
        ▼
Kafka Producer
        │
        ▼
Apache Kafka Broker
        │
 ┌──────┴─────────┐
 ▼                ▼
Worker 1      Worker 2
        │
        ▼
Processing Engine
        │
        ▼
Database
        │
        ▼
FastAPI
        │
        ▼
React Dashboard
        │
        ▼
Prometheus
        │
        ▼
Grafana

---

# Module Responsibilities

## Event Generator
Creates sample events.

## Kafka Producer
Publishes events to Kafka.

## Kafka Broker
Stores and distributes events.

## Workers
Consume and process events.

## Database
Stores processed information.

## FastAPI
Provides REST APIs.

## React
Displays dashboards.

## Prometheus
Collects metrics.

## Grafana
Visualizes metrics.

---

# Technology Stack

Backend:
- Python
- FastAPI
- SQLAlchemy

Streaming:
- Apache Kafka

Frontend:
- React

Monitoring:
- Prometheus
- Grafana

Deployment:
- Docker

Version Control:
- Git
- GitHub

---

# Future Enhancements

- Authentication
- Multiple Topics
- Event Replay
- Cloud Deployment
- Kubernetes