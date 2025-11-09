from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Incident Management API",
    description="API service for managing incidents from various sources",
    version="1.0.0"
)

@app.post("/api/incidents",
          response_model=schemas.IncidentResponse,
          status_code=201,
          summary="Create a new incident")
def create_incident(
    incident: schemas.IncidentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new incident with the following information:
    - **description**: A detailed description of the incident
    - **source**: The source of the incident (operator/monitoring/partner)
    - **status**: The initial status (defaults to "new")
    """
    return crud.create_incident(db=db, incident=incident)

@app.get("/api/incidents",
         response_model=List[schemas.IncidentResponse],
         summary="Get list of incidents")
def list_incidents(
    status: Optional[models.IncidentStatus] = Query(None, description="Filter by incident status"),
    skip: int = Query(0, ge=0, description="Number of incidents to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of incidents to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of incidents with optional status filtering.
    You can paginate results using skip and limit parameters.
    """
    return crud.get_incidents(db=db, status=status, skip=skip, limit=limit)

@app.patch("/api/incidents/{incident_id}",
           response_model=schemas.IncidentResponse,
           summary="Update incident status")
def update_incident_status(
    incident_id: int,
    status_update: schemas.IncidentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of an incident by its ID.
    Returns 404 if the incident is not found.
    """
    incident = crud.get_incident(db=db, incident_id=incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return crud.update_incident_status(db=db, incident=incident, status_update=status_update)