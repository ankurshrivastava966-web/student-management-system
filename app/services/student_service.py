
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


def create_student(db: Session, data: StudentCreate) -> Student:
    student = Student(**data.model_dump())
    db.add(student)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        raise


def list_students(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
) -> tuple[list[Student], int]:
    query = select(Student)

    if search:
        term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Student.name.ilike(term),
                Student.email.ilike(term),
                Student.course.ilike(term),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = db.scalar(count_query) or 0

    query = (
        query.order_by(Student.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )

    students = list(db.scalars(query).all())
    return students, total


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def update_student(
    db: Session,
    student: Student,
    data: StudentUpdate,
) -> Student:
    changes = data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if value is None:
            raise ValueError(f"{field} cannot be null")
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        raise


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()