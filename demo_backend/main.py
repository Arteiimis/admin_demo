from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .schemas import student_schema, user_schema
from .models import student_model
from .auth import authop
from . import crud
from .db.database import SessionLocal, engine

app = FastAPI()

student_model.Base.metadata.create_all(bind=engine)

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


@app.post("/students/", response_model=student_schema.Student)
def create_student(student: student_schema.StudentCreate, db: Session = Depends(get_db)):
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


@app.put("/students/{student_id}", response_model=student_schema.Student)
def update_student(student_id: int, student: student_schema.StudentUpdate, db: Session = Depends(get_db)):
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


@app.get("/students/", response_model=list[student_schema.Student])
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


@app.get("/students/{student_id}", response_model=student_schema.Student)
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


@app.get("/students/byname/{name}", response_model=student_schema.Student)
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


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> user_schema.Token:
    """
    Authenticates the user and generates an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.

    Returns:
        Token: The access token and its type.
    """
    user = authop.authenticate_user(authop.fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=authop.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authop.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return user_schema.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=user_schema.User)
async def read_users_me(current_user: Annotated[user_schema.User, Depends(authop.get_current_user)]):
    """
    Retrieve the currently authenticated user.

    Parameters:
    - current_user: The currently authenticated user.

    Returns:
    - The currently authenticated user.
    """
    return current_user


@app.get("/user/me/items/")
async def read_own_items(current_user: Annotated[user_schema.User, Depends(authop.get_current_user)]):
    """
    Retrieve the items owned by the current user.

    Parameters:
    - current_user: The authenticated user.

    Returns:
    - A list of dictionaries representing the items owned by the current user.
        Each dictionary contains the item_id and owner information.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/")
async def root():
    return {"message": "Hello World"}
