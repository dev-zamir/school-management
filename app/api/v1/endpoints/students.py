import math

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.pagination import PaginationParams
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    PaginatedStudentResponse,
)
from app.services import student as student_service

router = APIRouter()


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student",
)
async def create_student(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.create_student(db, data)


@router.get(
    "/",
    response_model=PaginatedStudentResponse,
    summary="List students with pagination",
)
async def list_students(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
):
    students, total = await student_service.list_students(db, pagination)
    return PaginatedStudentResponse(
        items=students,
        total=total,
        page=pagination.page,
        per_page=pagination.per_page,
        pages=math.ceil(total / pagination.per_page),
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by ID",
)
async def get_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.get_student(db, student_id)


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student",
)
async def update_student(
    student_id: UUID,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await student_service.update_student(db, student_id, data)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
)
async def delete_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await student_service.delete_student(db, student_id)
