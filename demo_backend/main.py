from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 配置CORS中间件
origins = [
    "http://localhost:5173",  # 允许的前端URL
    # 你可以在这里添加更多的允许的源
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student in the database.

    Args:
        student (schemas.StudentCreate): The student data to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.Student: The created student.

    Raises:
        HTTPException: If the student is already registered.
    """
    db_student = crud.get_student(db, student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student already registered")

    return crud.create_student(db=db, student=student)


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Delete a student from the database.

    Args:
        student_id (int): The ID of the student to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a message indicating the success of the deletion.

    Raises:
        HTTPException: If the student with the given ID is not found in the database.
    """
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    crud.delete_student(db, student_id)
    return {"message": "Student deleted"}


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """
    Update a student in the database.

    Args:
        student_id (int): The ID of the student to update.
        student (schemas.StudentUpdate): The updated student data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.Student: The updated student.

    Raises:
        HTTPException: If the student is not found in the database.
    """
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return db_student


@app.get("/students/", response_model=list[schemas.Student])
def read_students(db: Session = Depends(get_db)):
    """
    Retrieve all students from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Student]: A list of student objects.
    """
    students = crud.get_students(db)
    return students


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a student from the database by their ID.

    Args:
        student_id (int): The ID of the student to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The student information.

    Raises:
        HTTPException: If the student is not found in the database.
    """
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return db_student


@app.get("/students/byname/{name}", response_model=schemas.Student)
def read_student_byname(name: str, db: Session = Depends(get_db)):
    """
    Retrieve a student from the database by their name.

    Args:
        name (str): The name of the student to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The student information.

    Raises:
        HTTPException: If the student is not found in the database.
    """
    db_student = crud.get_student_byname(db, name)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return db_student


@app.get("/")
async def root():
    return {"message": "Hello World"}
