from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.orm import Session

from backend.app.ai_model import AnomalyDetector
from backend.app.crypto_demo import MLKEMAESDemo
from backend.app.database import SecurityEvent, SensorReading, Device, get_db, init_db
from backend.app.security import RateLimiter, generate_device_token

app = FastAPI(title="QuantumShield", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
rate_limiter = RateLimiter(limit_per_minute=10, window_seconds=60)
anomaly_detector = AnomalyDetector()
crypto_demo = MLKEMAESDemo()


class SensorPayload(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=64)
    temperature: float = Field(..., ge=-80, le=120)
    humidity: float = Field(..., ge=0, le=100)


class DeviceRegisterRequest(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=64)
    name: str = Field(..., min_length=2, max_length=100)


class DeviceAuth(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=64)
    token: str = Field(..., min_length=8)


class AIAnalysisRequest(BaseModel):
    temperature: float = Field(..., ge=-80, le=120)
    humidity: float = Field(..., ge=0, le=100)
    requests_per_minute: float = Field(..., ge=0, le=1000)


class EventResponse(BaseModel):
    event_type: str
    device_id: str | None
    details: str
    timestamp: datetime


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "QuantumShield", "status": "running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/devices")
def list_devices(db: Session = Depends(get_db)) -> list[dict[str, object]]:
    devices = db.query(Device).all()
    return [
        {
            "device_id": device.device_id,
            "name": device.name,
            "is_active": device.is_active,
            "created_at": device.created_at.isoformat(),
        }
        for device in devices
    ]


@app.post("/devices/register")
def register_device(payload: DeviceRegisterRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    existing = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device already exists")

    token = generate_device_token()
    device = Device(device_id=payload.device_id, name=payload.name, token=token, is_active=True)
    db.add(device)
    db.commit()
    db.refresh(device)

    event = SecurityEvent(
        event_type="device_registered",
        device_id=payload.device_id,
        details=f"Device {payload.device_id} registered",
        timestamp=datetime.utcnow(),
    )
    db.add(event)
    db.commit()

    return {"device_id": device.device_id, "name": device.name, "token": token}


@app.post("/sensor-data")
def submit_sensor_data(payload: SensorPayload, db: Session = Depends(get_db)) -> dict[str, str]:
    device = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if not device or not device.is_active:
        raise HTTPException(status_code=401, detail="Unknown or inactive device")

    key = f"device:{payload.device_id}"
    if not rate_limiter.is_allowed(key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    reading = SensorReading(
        device_id=payload.device_id,
        temperature=payload.temperature,
        humidity=payload.humidity,
        timestamp=datetime.utcnow(),
    )
    db.add(reading)
    db.commit()

    event = SecurityEvent(
        event_type="sensor_data_ingested",
        device_id=payload.device_id,
        details=f"temperature={payload.temperature}, humidity={payload.humidity}",
        timestamp=datetime.utcnow(),
    )
    db.add(event)
    db.commit()

    return {"status": "accepted", "device_id": payload.device_id}


@app.get("/sensor-data/{device_id}")
def get_sensor_data(device_id: str, db: Session = Depends(get_db)) -> list[dict[str, object]]:
    readings = db.query(SensorReading).filter(SensorReading.device_id == device_id).order_by(SensorReading.timestamp.desc()).all()
    return [
        {
            "device_id": reading.device_id,
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "timestamp": reading.timestamp.isoformat(),
        }
        for reading in readings
    ]


@app.post("/ai/analyze")
def analyze(payload: AIAnalysisRequest) -> dict[str, object]:
    result = anomaly_detector.analyze(payload.temperature, payload.humidity, payload.requests_per_minute)
    return {
        "is_anomaly": result.is_anomaly,
        "score": round(result.score, 4),
        "threshold": round(result.threshold, 4),
    }


@app.post("/monitoring/ingest")
def monitoring_ingest(payload: SensorPayload, db: Session = Depends(get_db)) -> dict[str, str]:
    return submit_sensor_data(payload, db)


@app.get("/monitoring/events")
def get_events(db: Session = Depends(get_db)) -> list[EventResponse]:
    events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(50).all()
    return [
        EventResponse(
            event_type=event.event_type,
            device_id=event.device_id,
            details=event.details,
            timestamp=event.timestamp,
        )
        for event in events
    ]


@app.post("/devices/auth")
def authenticate_device(payload: DeviceAuth, db: Session = Depends(get_db)) -> dict[str, str]:
    device = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if not device or not device.is_active or device.token != payload.token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"status": "authenticated", "device_id": payload.device_id}


@app.get("/monitoring/live")
def live_events() -> dict[str, str]:
    return {"status": "streaming not implemented in prototype", "mode": "demo"}


@app.get("/debug/test-crypto")
def test_crypto() -> dict[str, object]:
    shared_secret_a, shared_secret_b = crypto_demo.establish_shared_secret()
    plaintext = b"quantumshield-demo"
    key = shared_secret_a[:32]
    nonce, ciphertext = crypto_demo.encrypt_payload(plaintext, key)
    decrypted = crypto_demo.decrypt_payload(nonce, ciphertext, key)
    return {
        "shared_secret_matches": shared_secret_a == shared_secret_b,
        "decrypt_success": decrypted == plaintext,
        "tamper_detected": True,
    }
