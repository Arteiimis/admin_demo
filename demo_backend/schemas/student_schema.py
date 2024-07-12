from datetime import datetime
from pydantic import BaseModel


class StudentBase(BaseModel):
    student_id: int
    name: str
    major: str
    status: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    name: str | None
    major: str | None
    status: str | None


class Student(StudentBase):
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
