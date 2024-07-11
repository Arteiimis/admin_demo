from sqlalchemy.orm import Session
import models
import database
import schemas


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, major=student.major, status=student.status)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db.query(models.Student).filter(models.Student.student_id == student_id).delete()
    db.commit()


def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if db_student is None:
        return None

    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()


def get_student_byname(db: Session, name: str):
    return db.query(models.Student).filter(models.Student.name == name).first()
