# IoT Cloud Platform — GSoC Proof of Concept

A lightweight, open-source IoT cloud platform demonstrating secure device authentication, telemetry ingestion, persistent storage, and visualization.

## Features
- **Device Authentication & Registration**: Devices can register securely and obtain unique, persistent API keys.
- **Telemetry Ingestion**: Devices ingest JSON telemetry data validated via Pydantic using their API keys.
- **Persistent Storage**: Data is stored reliably in a structured, time-series format using SQLite and SQLAlchemy.
- **Dashboard Visualization**: A sleek, modern, interactive web-based dashboard powered by Chart.js runs locally to visualize real-time device telemetry.

## Stack
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy (SQLite)
- **Frontend:** HTML, CSS, JavaScript (Chart.js)
- **Validation:** Pydantic

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic requests
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **View the Dashboard:**
   Open your browser to `http://localhost:8000/`

4. **API Interactive Docs:**
   Available at `http://localhost:8000/docs`

## Test the API Workflows

We provide a Python script to automate the flow of registering a device and ingesting data:

```bash
python test_api.py
```

### Manual Testing via cURL:

**1. Register a new device:**
```bash
curl -X POST http://localhost:8000/v1/devices \
  -H "Content-Type: application/json" \
  -d '{"name": "Living Room Sensor"}'
```
*(Copy the generated `api_key` for the next steps)*

**2. POST telemetry (authorized device):**
```bash
curl -X POST http://localhost:8000/v1/telemetry \
  -H "X-Device-Token: <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"values": {"temperature": 22.5, "humidity": 60}}'
```

**3. GET stored telemetry:**
```bash
curl http://localhost:8000/v1/telemetry
```

## Project Structure
```text
GSoC/
├── main.py         ← FastAPI backend server, REST routes
├── database.py     ← SQLite configuration & SQLAlchemy Models
├── models.py       ← Pydantic validation schemas
├── test_api.py     ← E2E Python test script
├── iot_cloud.db    ← Auto-generated SQLite database
└── static/         ← Frontend Dashboard
    ├── index.html  ← Dashboard HTML structure
    ├── style.css   ← Premium dark-mode styling
    └── app.js      ← Data fetch and Chart.js initialization
```

## GSoC Context
This project is a functional, educational proof-of-concept for the GSoC proposal:  
**"Minimal Educational IoT Cloud Platform"** — explicitly demonstrating the entire hardware-to-cloud lifecycle: registration, secure ingestion, database storage, and frontend visualization.
