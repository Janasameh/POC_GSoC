from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
import database
import models

app = FastAPI(title="GSoC IoT Cloud POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
database.init_db()

# Serve static files for dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/v1/devices", response_model=models.DeviceResponse)
def register_device(device: models.DeviceCreate, db: Session = Depends(database.get_db)):
    """Register a new device and receive an API key"""
    device_id = f"dev-{uuid.uuid4().hex[:8]}"
    api_key = f"key-{uuid.uuid4().hex}"
    
    db_device = database.Device(id=device_id, api_key=api_key, name=device.name)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.post("/v1/telemetry")
def ingest_data(request: Request, data: models.TelemetrySchema, db: Session = Depends(database.get_db)):
    """Ingest telemetry data from an authenticated device"""
    api_key = request.headers.get("X-Device-Token")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-Device-Token header")
        
    device = db.query(database.Device).filter(database.Device.api_key == api_key).first()
    if not device:
        raise HTTPException(status_code=401, detail="Unauthorized Device")
        
    db_telemetry = database.Telemetry(device_id=device.id, payload=data.values)
    db.add(db_telemetry)
    db.commit()
    return {"status": "ok", "message": "Telemetry ingested successfully"}

@app.get("/v1/telemetry", response_model=list[models.TelemetryResponse])
def get_telemetry(db: Session = Depends(database.get_db), limit: int = 100):
    """Fetch stored telemetry data for the dashboard"""
    telemetry = db.query(database.Telemetry).order_by(database.Telemetry.received_at.desc()).limit(limit).all()
    # Reverse to return older -> newer for Chart.js rendering
    return list(reversed(telemetry))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
