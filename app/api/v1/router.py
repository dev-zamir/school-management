from fastapi import APIRouter

# As you build each phase, import and include routers here
# from app.api.v1.endpoints import students, teachers, auth, classes

api_router = APIRouter()

# --- Phase 1: Uncomment as you build ---
# api_router.include_router(students.router, prefix="/students", tags=["Students"])
# api_router.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
# api_router.include_router(auth.router,     prefix="/auth",     tags=["Auth"])
# api_router.include_router(classes.router,  prefix="/classes",  tags=["Classes"])
