from sqlalchemy import Column, String, Date, Integer, Boolean

from app.db.session import Base
from app.models.base import UUIDMixin, TimestampMixin


class Student(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "students"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    grade_level = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
