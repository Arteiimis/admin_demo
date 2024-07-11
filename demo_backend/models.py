import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    major = sa.Column(sa.String, index=True)
    status = sa.Column(sa.String, index=True)

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
