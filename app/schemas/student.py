from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date, datetime
from uuid import UUID
from typing import Optional


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    date_of_birth: date
    grade_level: int = Field(..., ge=1, le=12)
    is_active: bool = True


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    grade_level: Optional[int] = Field(None, ge=1, le=12)
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class PaginatedStudentResponse(BaseModel):
    items: list[StudentResponse]
    total: int
    page: int
    per_page: int
    pages: int
