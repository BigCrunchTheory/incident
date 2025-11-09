from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .models import IncidentStatus, IncidentSource

class IncidentBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=1000)
    source: IncidentSource

class IncidentCreate(IncidentBase):
    status: IncidentStatus = IncidentStatus.NEW

class IncidentUpdate(BaseModel):
    status: IncidentStatus

class IncidentResponse(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True