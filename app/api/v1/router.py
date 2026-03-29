from fastapi import APIRouter

from app.api.v1.endpoints import students

api_router = APIRouter()

api_router.include_router(students.router, prefix="/students", tags=["Students"])

# --- Future phases ---
# api_router.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
# api_router.include_router(auth.router,     prefix="/auth",     tags=["Auth"])
# api_router.include_router(classes.router,  prefix="/classes",  tags=["Classes"])
