# IoT Cloud Platform — GSoC Proof of Concept

A lightweight, open-source IoT cloud platform demonstrating secure device authentication and telemetry ingestion.

## Features
- Device authentication via API keys (`X-Device-Token`)
- Telemetry ingestion with JSON validation
- In-memory storage (SQLite integration planned)
- CORS-enabled REST API
- Interactive API docs via Swagger UI

## Stack
- **Backend:** Python, FastAPI, Uvicorn
- **Validation:** Pydantic
- **Planned:** SQLite/PostgreSQL, Chart.js dashboard

## Quickstart

```bash
pip install fastapi uvicorn
python Snippet.py
```

Server runs at: `http://localhost:8000`  
Swagger UI at: `http://localhost:8000/docs`

## Test the API

**POST telemetry (authorized device):**
```bash
curl -X POST http://localhost:8000/v1/telemetry \
  -H "X-Device-Token: secret-device-key-123" \
  -H "Content-Type: application/json" \
  -d '{"values": {"temperature": 22.5, "humidity": 60}}'
```

**GET stored telemetry:**
```bash
curl http://localhost:8000/v1/telemetry
```

## Valid Test API Keys
| Key | Device ID |
|-----|-----------|
| `secret-device-key-123` | `device-001` |
| `secret-device-key-456` | `device-002` |

## Project Structure
```
GSoC/
├── Snippet.py   ← FastAPI backend
└── README.md
```

## GSoC Context
This project is a proof of concept for the GSoC proposal:  
**"Minimal Educational IoT Cloud Platform"** — demonstrating the core ingestion + auth pattern used by platforms like AWS IoT and Azure IoT Hub.
