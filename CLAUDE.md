# School Management System — Claude Code Instructions

## Project Overview
A FastAPI-based School Management System API built for learning FastAPI deeply.
No frontend — all testing is done via Swagger UI at `/docs`.

## Tech Stack
- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL (async via asyncpg + SQLAlchemy 2.0)
- **Migrations:** Alembic
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **Background Jobs:** Celery + Redis
- **Testing:** pytest + pytest-asyncio + httpx

## Project Structure
```
app/
├── main.py                  # App entry point, middleware, router registration
├── api/
│   └── v1/
│       ├── router.py        # Aggregates all endpoint routers
│       └── endpoints/       # One file per resource (students.py, teachers.py, etc.)
├── core/
│   ├── config.py            # Settings via pydantic-settings (.env)
│   └── exceptions.py        # Custom HTTP exceptions
├── db/
│   └── session.py           # Async engine, session factory, get_db dependency
├── models/                  # SQLAlchemy ORM models
├── schemas/                 # Pydantic request/response schemas
├── services/                # Business logic layer (one file per domain)
├── dependencies/            # Reusable FastAPI dependencies (auth, pagination, etc.)
├── utils/                   # Pure helper functions
└── tasks/                   # Celery tasks
tests/
├── api/                     # Endpoint integration tests
├── services/                # Service layer unit tests
└── unit/                    # Schema and utility tests
```

## Conventions
- **Async everywhere:** All endpoints, DB calls, and services must be `async def`
- **Dependency Injection:** Use `Depends()` for DB session, auth, pagination — never import session directly in endpoints
- **Service Layer:** Endpoints should only handle HTTP concerns. All business logic lives in `services/`
- **Schemas separate from Models:** Never return ORM models directly — always use Pydantic response schemas
- **Versioning:** All routes are prefixed with `/api/v1/`
- **Exceptions:** Use custom exceptions from `app.core.exceptions` — never raise raw HTTPException in endpoints

## Adding a New Resource (Pattern to follow)
1. Create SQLAlchemy model in `app/models/<resource>.py`
2. Create Pydantic schemas in `app/schemas/<resource>.py` (Base, Create, Update, Response)
3. Create service in `app/services/<resource>.py`
4. Create endpoint router in `app/api/v1/endpoints/<resource>.py`
5. Register router in `app/api/v1/router.py`
6. Generate Alembic migration: `alembic revision --autogenerate -m "add <resource>"`

## Running Locally
```bash
# Start dependencies
docker-compose up db redis -d

# Install deps
pip install -r requirements.txt

# Copy env
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload

# Swagger UI
open http://localhost:8000/docs
```

## Running Tests
```bash
pytest tests/ -v
```

## Learning Phases (refer to roadmap.md)
- Phase 1: Fundamentals — routing, Pydantic, Swagger
- Phase 2: DB — SQLAlchemy async, Alembic
- Phase 3: Dependency Injection — Depends(), nested deps
- Phase 4: Auth — JWT, RBAC
- Phase 5: Business Logic — services, exceptions
- Phase 6: Background Tasks — Celery, BackgroundTasks
- Phase 7: File Uploads
- Phase 8: WebSockets
- Phase 9: Testing
- Phase 10: Production patterns
