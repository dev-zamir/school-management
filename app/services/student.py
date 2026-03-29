import math
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.core.exceptions import StudentNotFoundError, AlreadyExistsError
from app.dependencies.pagination import PaginationParams


async def create_student(db: AsyncSession, data: StudentCreate) -> Student:
    existing = await db.execute(
        select(Student).where(Student.email == data.email)
    )
    if existing.scalar_one_or_none():
        raise AlreadyExistsError("Student", "email", data.email)

    student = Student(**data.model_dump())
    db.add(student)
    await db.flush()
    await db.refresh(student)
    return student


async def get_student(db: AsyncSession, student_id: UUID) -> Student:
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise StudentNotFoundError(str(student_id))
    return student


async def list_students(
    db: AsyncSession, pagination: PaginationParams
) -> tuple[list[Student], int]:
    count_result = await db.execute(select(func.count(Student.id)))
    total = count_result.scalar()

    result = await db.execute(
        select(Student)
        .order_by(Student.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    students = list(result.scalars().all())
    return students, total


async def update_student(
    db: AsyncSession, student_id: UUID, data: StudentUpdate
) -> Student:
    student = await get_student(db, student_id)
    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != student.email:
        existing = await db.execute(
            select(Student).where(Student.email == update_data["email"])
        )
        if existing.scalar_one_or_none():
            raise AlreadyExistsError("Student", "email", update_data["email"])

    for field, value in update_data.items():
        setattr(student, field, value)

    await db.flush()
    await db.refresh(student)
    return student


async def delete_student(db: AsyncSession, student_id: UUID) -> None:
    student = await get_student(db, student_id)
    await db.delete(student)
    await db.flush()
