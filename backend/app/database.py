from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "quantumshield.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(index=True, nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(index=True, nullable=False)
    device_id: Mapped[str | None] = mapped_column(index=True, nullable=True)
    details: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
