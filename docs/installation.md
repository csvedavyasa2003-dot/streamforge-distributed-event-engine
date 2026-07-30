# Installation Guide

## Prerequisites

- Python 3.12+
- Git
- Node.js
- Docker Desktop
- VS Code

---

## Clone Repository

```bash
git clone https://github.com/csvedavyasa2003-dot/streamforge-distributed-event-engine.git
```

---

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## Frontend

```bash
cd frontend

npm install

npm start
```

---

## Kafka

Install Docker Desktop

Start Kafka using Docker Compose.

---

## Monitoring

Start Prometheus

Start Grafana