from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from enum import Enum as PyEnum

from .database import Base

class IncidentStatus(str, PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class IncidentSource(str, PyEnum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(
        String,
        nullable=False,
        default=IncidentStatus.NEW
    )
    source = Column(
        String,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)