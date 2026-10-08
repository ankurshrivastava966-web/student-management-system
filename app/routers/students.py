
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import StudentCreate, StudentResponse, StudentUpdate
from app.services import student_service


router = APIRouter(prefix="/students", tags=["Students"])

DBSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(data: StudentCreate, db: DBSession):
    try:
        return student_service.create_student(db, data)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )


@router.get("/")
def list_students(
    db: DBSession,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
):
    students, total = student_service.list_students(
        db,
        page=page,
        limit=limit,
        search=search,
    )

    return {
        "items": students,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: DBSession):
    student = student_service.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: DBSession,
):
    student = student_service.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if not data.model_fields_set:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update",
        )

    try:
        return student_service.update_student(db, student, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )


@router.delete("/{student_id}")
def delete_student(student_id: int, db: DBSession):
    student = student_service.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student_service.delete_student(db, student)

    return {"message": "Student deleted successfully"}