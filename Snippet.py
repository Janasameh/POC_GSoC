from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins (fine for local dev)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Schema
# ----------------------------

class TelemetrySchema(BaseModel):
    values: Dict[str, Any]  # e.g. {"temperature": 22.5, "humidity": 60}


# ----------------------------
# Simulated In-Memory DB Layer
# ----------------------------

class Device:
    def __init__(self, id: str):
        self.id = id

class FakeDB:
    def __init__(self):
        # Pre-registered API keys → device IDs
        self._keys = {
            "secret-device-key-123": Device(id="device-001"),
            "secret-device-key-456": Device(id="device-002"),
        }
        self._telemetry: List[Dict] = []

    async def verify_key(self, api_key: Optional[str]) -> Optional[Device]:
        return self._keys.get(api_key)

    async def save_telemetry(self, payload: Dict) -> Dict:
        self._telemetry.append(payload)
        return {"status": "ok", "saved": payload}

    async def get_all(self) -> List[Dict]:
        return self._telemetry


db = FakeDB()


# ----------------------------
# Endpoint
# ----------------------------

@app.post("/v1/telemetry")
async def ingest_data(request: Request, data: TelemetrySchema):
    # 1. Extract API Key from Header
    api_key = request.headers.get("X-Device-Token")

    # 2. Authenticate Device
    device = await db.verify_key(api_key)
    if not device:
        raise HTTPException(status_code=401, detail="Unauthorized Device")

    # 3. Store with Timestamp
    payload = {
        "device_id": device.id,
        "payload": data.values,
        "received_at": datetime.utcnow().isoformat(),
    }
    return await db.save_telemetry(payload)


# Bonus: view stored telemetry
@app.get("/v1/telemetry")
async def get_telemetry():
    return await db.get_all()


# ----------------------------
# Run
# ----------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
