# GET /courses and so on
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    """Return all courses."""
    courses = db.query(Course).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "credits": c.credits,
            "description": c.description,
        }
        for c in courses
    ]

@router.get("/{course_id}")
def get_course(course_id: str, db: Session = Depends(get_db)):
    """Return a single course by ID."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "id": course.id,
        "name": course.name,
        "credits": course.credits,
        "description": course.description,
    }

@router.get("/{course_id}/prerequisites")
def get_prerequisites(course_id: str, db: Session = Depends(get_db)):
    """Return the prerequisites for a course."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    prereq_ids = [p.prereq_id for p in course.prerequisites]
    prereqs = db.query(Course).filter(Course.id.in_(prereq_ids)).all()

    return {
        "course_id": course_id,
        "prerequisites": [
            {"id": c.id, "name": c.name, "credits": c.credits}
            for c in prereqs
        ],
    }