from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str

class DeviceResponse(BaseModel):
    id: str
    api_key: str
    name: str
    registered_at: datetime
    
    class Config:
        from_attributes = True

class TelemetrySchema(BaseModel):
    values: Dict[str, Any]

class TelemetryResponse(BaseModel):
    id: int
    device_id: str
    payload: Dict[str, Any]
    received_at: datetime
    
    class Config:
        from_attributes = True
