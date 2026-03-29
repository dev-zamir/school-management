# School Management System — Learning Roadmap

> A phased approach to learning FastAPI deeply by building a real project.
> Each phase builds on the previous one. No frontend — test everything via Swagger UI (`/docs`).

---

## Phase 0: Project Scaffolding (DONE)

**Goal:** Set up the project skeleton so every future phase has a clear place to land.

**Completed:**
- [x] FastAPI app with CORS middleware (`app/main.py`)
- [x] Async PostgreSQL setup with SQLAlchemy 2.0 (`app/db/session.py`)
- [x] Alembic migrations directory
- [x] Pydantic Settings + `.env` config (`app/core/config.py`)
- [x] Custom exception hierarchy (`app/core/exceptions.py`)
- [x] Base model mixins: `UUIDMixin`, `TimestampMixin` (`app/models/base.py`)
- [x] `PaginationParams` dependency (`app/dependencies/`)
- [x] Docker Compose (PostgreSQL + Redis)
- [x] Test directory structure + pytest config
- [x] `requirements.txt` with all dependencies

---

## Phase 1: Fundamentals — Routing, Pydantic, Swagger

**Goal:** Learn how FastAPI handles requests, validation, and auto-generates docs.

**Tasks:**
- [ ] Create the `Student` model (`app/models/student.py`) with fields: `first_name`, `last_name`, `email`, `date_of_birth`, `grade_level`, `is_active`
- [ ] Create Pydantic schemas (`app/schemas/student.py`): `StudentBase`, `StudentCreate`, `StudentUpdate`, `StudentResponse`
- [ ] Create a basic service (`app/services/student.py`) with CRUD operations
- [ ] Create the students endpoint router (`app/api/v1/endpoints/students.py`):
  - `POST /api/v1/students` — create a student
  - `GET /api/v1/students` — list students (with pagination)
  - `GET /api/v1/students/{id}` — get a single student
  - `PUT /api/v1/students/{id}` — update a student
  - `DELETE /api/v1/students/{id}` — delete a student
- [ ] Register the router in `app/api/v1/router.py`
- [ ] Generate and run the first Alembic migration
- [ ] Test all endpoints manually via Swagger UI

**Key Concepts:**
- Path parameters, query parameters, request bodies
- Pydantic validation (field constraints, `EmailStr`, optional fields)
- Response models and status codes
- Auto-generated OpenAPI docs

---

## Phase 2: Database — SQLAlchemy Async + Alembic

**Goal:** Master async database operations, relationships, and migrations.

**Tasks:**
- [ ] Create the `Teacher` model with fields: `first_name`, `last_name`, `email`, `subject_specialization`, `hire_date`, `is_active`
- [ ] Create the `Class` model with fields: `name`, `class_code`, `teacher_id` (FK), `max_students`, `schedule`, `room_number`
- [ ] Create the `Enrollment` model (many-to-many: Student <-> Class) with fields: `student_id`, `class_id`, `enrollment_date`, `status`
- [ ] Set up SQLAlchemy relationships (`relationship()`, `back_populates`)
- [ ] Build full CRUD for teachers and classes (schemas, services, endpoints)
- [ ] Enrollment endpoints:
  - `POST /api/v1/enrollments` — enroll a student in a class
  - `GET /api/v1/classes/{id}/students` — list students in a class
  - `GET /api/v1/students/{id}/classes` — list classes for a student
  - `DELETE /api/v1/enrollments/{id}` — drop a student from a class
- [ ] Practice Alembic: create migration, modify a column, add an index
- [ ] Use `selectinload` / `joinedload` for eager loading related data

**Key Concepts:**
- Async `select()`, `insert()`, `update()`, `delete()` with SQLAlchemy 2.0
- Foreign keys and relationships
- Many-to-many via association table
- Eager vs lazy loading
- Alembic autogenerate, manual edits, upgrade/downgrade

---

## Phase 3: Dependency Injection — Depends()

**Goal:** Understand how FastAPI's DI system works and build reusable dependencies.

**Tasks:**
- [ ] Refactor: extract common query filters into dependencies (e.g., `ActiveFilterParam`, `SearchParam`)
- [ ] Create a `get_student_or_404` dependency that fetches a student by ID or raises `NotFoundError`
- [ ] Create similar `get_teacher_or_404`, `get_class_or_404` dependencies
- [ ] Build a `SortingParams` dependency (sort_by, sort_order) and apply to list endpoints
- [ ] Create a `CurrentUserDep` placeholder dependency (returns a dummy user for now — wired up in Phase 4)
- [ ] Demonstrate nested dependencies: `get_enrollment_or_404` depends on both `get_student_or_404` and `get_class_or_404`

**Key Concepts:**
- `Depends()` for function, class, and generator dependencies
- Dependency caching (same request reuse)
- Nested / chained dependencies
- Overriding dependencies in tests

---

## Phase 4: Auth — JWT + RBAC

**Goal:** Secure the API with token-based authentication and role-based access.

**Tasks:**
- [ ] Create `User` model with fields: `email`, `hashed_password`, `role` (enum: `admin`, `teacher`, `student`), `is_active`
- [ ] Implement password hashing with passlib/bcrypt
- [ ] Create auth endpoints:
  - `POST /api/v1/auth/register` — register a new user
  - `POST /api/v1/auth/login` — returns access + refresh JWT tokens
  - `POST /api/v1/auth/refresh` — refresh an expired access token
  - `GET /api/v1/auth/me` — get current user profile
- [ ] Build `get_current_user` dependency (decode JWT, fetch user from DB)
- [ ] Build `require_role(roles)` dependency for role-based access
- [ ] Apply auth to existing endpoints:
  - Anyone can read public data
  - Only `admin` can create/delete teachers and classes
  - Only `admin` and `teacher` can manage enrollments
  - Students can only view their own data
- [ ] Add `created_by` / `updated_by` tracking to models

**Key Concepts:**
- JWT access + refresh token flow
- Password hashing (never store plaintext)
- `Security` dependencies and OAuth2 scheme
- Role-based access control patterns
- Token expiration and refresh logic

---

## Phase 5: Business Logic — Services + Exceptions

**Goal:** Build real business rules and learn to handle domain-specific errors cleanly.

**Tasks:**
- [ ] Enforce class capacity: raise `ClassFullError` when `max_students` is reached
- [ ] Prevent duplicate enrollments: raise `DuplicateEnrollmentError`
- [ ] Add a `Grade` model and grading endpoints:
  - `POST /api/v1/grades` — assign a grade (only the class teacher can grade)
  - `GET /api/v1/students/{id}/grades` — get all grades for a student
  - `GET /api/v1/students/{id}/gpa` — calculate GPA
- [ ] Implement student transfer between classes (drop + enroll in a transaction)
- [ ] Add an `Attendance` model and endpoints:
  - `POST /api/v1/attendance` — mark attendance for a class session
  - `GET /api/v1/students/{id}/attendance` — attendance summary
- [ ] Ensure all business logic lives in the service layer, not in endpoints
- [ ] Use database transactions for multi-step operations

**Key Concepts:**
- Service layer as the single source of business rules
- Custom exception classes for domain errors
- Transaction management (`async with session.begin()`)
- Computed/derived data (GPA calculation)
- Separation of concerns: endpoints = HTTP, services = logic

---

## Phase 6: Background Tasks — Celery + BackgroundTasks

**Goal:** Offload slow or non-critical work to background processing.

**Tasks:**
- [ ] Set up Celery worker with Redis broker (`app/tasks/`)
- [ ] Create tasks:
  - `send_welcome_email` — triggered on student registration
  - `generate_report_card` — generates a PDF-like summary for a student
  - `send_attendance_alert` — notify when attendance drops below threshold
- [ ] Use FastAPI's `BackgroundTasks` for lightweight work:
  - Log audit trail entries after create/update/delete operations
- [ ] Create an `AuditLog` model to track who changed what and when
- [ ] Add endpoints to check task status:
  - `GET /api/v1/tasks/{task_id}/status` — poll Celery task status

**Key Concepts:**
- Celery task definition, calling, and result retrieval
- FastAPI `BackgroundTasks` vs Celery (when to use which)
- Redis as a message broker
- Task status polling
- Audit logging pattern

---

## Phase 7: File Uploads

**Goal:** Handle file uploads for profile photos and documents.

**Tasks:**
- [ ] Add a `profile_photo_url` field to Student and Teacher models
- [ ] Create upload endpoint:
  - `POST /api/v1/uploads/profile-photo` — upload and validate image files
- [ ] Validate file type (only images) and size (max 5MB)
- [ ] Store files locally in `/media/` (production would use S3)
- [ ] Serve uploaded files via a static files route
- [ ] Create a `Document` model for generic file attachments:
  - `POST /api/v1/documents` — upload a document (report card, transcript)
  - `GET /api/v1/documents/{id}` — download a document
- [ ] Bulk upload: accept multiple files in one request

**Key Concepts:**
- `UploadFile` and `File()` in FastAPI
- File validation (MIME type, size limits)
- Streaming large files
- Static file serving
- `python-multipart` for form data

---

## Phase 8: WebSockets

**Goal:** Add real-time features using WebSocket connections.

**Tasks:**
- [ ] Create a WebSocket endpoint for live class announcements:
  - `WS /api/v1/ws/class/{class_id}` — students connected get real-time announcements
- [ ] Build a simple notification system:
  - Teacher posts an announcement -> all connected students in that class receive it instantly
- [ ] Add connection management (track active connections, handle disconnects)
- [ ] Authenticate WebSocket connections using JWT (token passed as query param)
- [ ] Create a chat-like feature for class discussions:
  - `WS /api/v1/ws/chat/{class_id}` — real-time messaging within a class

**Key Concepts:**
- WebSocket lifecycle (connect, receive, send, disconnect)
- Connection manager pattern
- Broadcasting messages to groups
- WebSocket authentication
- Handling connection drops gracefully

---

## Phase 9: Testing

**Goal:** Write comprehensive tests and learn testing patterns for FastAPI.

**Tasks:**
- [ ] Set up test database (separate PostgreSQL database or SQLite for speed)
- [ ] Create test fixtures:
  - `async_client` — httpx `AsyncClient` for endpoint tests
  - `db_session` — test database session with rollback
  - `sample_student`, `sample_teacher`, `sample_class` — factory fixtures
  - `auth_headers` — pre-authenticated headers for different roles
- [ ] Write endpoint integration tests (`tests/api/`):
  - Test all CRUD operations for each resource
  - Test auth flows (register, login, protected routes)
  - Test error cases (404, 403, 422 validation errors)
- [ ] Write service layer unit tests (`tests/services/`):
  - Test business rules (class capacity, duplicate enrollment, GPA)
  - Test edge cases and error paths
- [ ] Write schema validation tests (`tests/unit/`):
  - Test Pydantic schema validation rules
- [ ] Override dependencies in tests (mock auth, mock services)
- [ ] Measure test coverage with `pytest-cov`

**Key Concepts:**
- `pytest-asyncio` for async test functions
- `httpx.AsyncClient` as the test client
- Fixtures and factory patterns
- Dependency overrides for isolation
- Testing error responses and edge cases
- Code coverage

---

## Phase 10: Production Patterns

**Goal:** Apply patterns that make the API production-ready.

**Tasks:**
- [ ] Add structured logging with request ID tracking
- [ ] Add rate limiting middleware (e.g., `slowapi`)
- [ ] Add response caching for read-heavy endpoints (Redis)
- [ ] Implement health check endpoint with DB connectivity check:
  - `GET /api/v1/health` — returns DB status, Redis status, uptime
- [ ] Add request/response logging middleware
- [ ] Configure CORS properly for specific origins
- [ ] Add API key authentication as an alternative auth method
- [ ] Set up Dockerfile for production (multi-stage build, gunicorn + uvicorn workers)
- [ ] Add OpenAPI metadata (tags, descriptions, examples for all endpoints)
- [ ] Implement soft delete pattern (set `is_active=False` instead of deleting rows)

**Key Concepts:**
- Middleware patterns (logging, rate limiting, CORS)
- Caching strategies
- Health checks and observability
- Production deployment with gunicorn
- API documentation best practices
- Soft delete vs hard delete

---

## Progress Tracker

| Phase | Status |
|-------|--------|
| 0 — Scaffolding | Done |
| 1 — Fundamentals | Not started |
| 2 — Database | Not started |
| 3 — Dependency Injection | Not started |
| 4 — Auth | Not started |
| 5 — Business Logic | Not started |
| 6 — Background Tasks | Not started |
| 7 — File Uploads | Not started |
| 8 — WebSockets | Not started |
| 9 — Testing | Not started |
| 10 — Production | Not started |
