# Incident Management API

A FastAPI-based service for managing incidents reported through various channels (operators, monitoring systems, partners).

## Features

- Create new incidents with description, source, and status
- List incidents with status filtering
- Update incident status by ID
- SQLite database for persistence
- Automatic API documentation
- Input validation
- Error handling

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd incident
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
alembic upgrade head
```

## Running the Service

Start the service with:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API Documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Create Incident
```http
POST /api/incidents
```
```json
{
    "description": "Self-service point offline",
    "source": "monitoring",
    "status": "new"
}
```

### List Incidents
```http
GET /api/incidents
GET /api/incidents?status=new
```

### Update Incident Status
```http
PATCH /api/incidents/{incident_id}
```
```json
{
    "status": "resolved"
}
```

## Status Values

- new
- in_progress
- resolved
- closed

## Source Values

- operator
- monitoring
- partner

## Running Tests

```bash
pytest
```

## Project Structure

```
incident/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── crud.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── alembic.ini
├── requirements.txt
└── README.md
```