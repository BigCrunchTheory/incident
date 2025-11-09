from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from . import models, schemas

def create_incident(db: Session, incident: schemas.IncidentCreate) -> models.Incident:
    db_incident = models.Incident(
        description=incident.description,
        status=incident.status,
        source=incident.source
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get_incidents(
    db: Session,
    status: Optional[models.IncidentStatus] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Incident]:
    query = db.query(models.Incident)
    if status:
        query = query.filter(models.Incident.status == status)
    return query.order_by(desc(models.Incident.created_at)).offset(skip).limit(limit).all()

def get_incident(db: Session, incident_id: int) -> Optional[models.Incident]:
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()

def update_incident_status(
    db: Session,
    incident: models.Incident,
    status_update: schemas.IncidentUpdate
) -> models.Incident:
    incident.status = status_update.status
    db.commit()
    db.refresh(incident)
    return incident