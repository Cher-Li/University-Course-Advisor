# GET /courses and so on
from fastapi import APIRouter

router = APIRouter(prefix="/courses", tags=["courses"])

# Stub data, replaced with real DB queries later
MOCK_COURSES = [
    {
        "id": "COMP250",
        "name": "Intro to Computer Science",
        "credits": 3,
        "prerequisites": [],
    },
    {
        "id": "COMP302",
        "name": "Programming Languages and Paradigms",
        "credits": 3,
        "prerequisites": ["COMP250"],
    },
    {
        "id": "COMP330",
        "name": "Theory of Computation",
        "credits": 3,
        "prerequisites": ["COMP250", "MATH240"],
    },
    {
        "id": "MATH240",
        "name": "Discrete Structures",
        "credits": 3,
        "prerequisites": [],
    },
]


@router.get("/")
def get_courses():
    """Return all courses."""
    return MOCK_COURSES


@router.get("/{course_id}")
def get_course(course_id: str):
    """Return a single course by ID."""
    course = next((c for c in MOCK_COURSES if c["id"] == course_id), None)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/prerequisites")
def get_prerequisites(course_id: str):
    """Return the prerequisites for a course."""
    course = next((c for c in MOCK_COURSES if c["id"] == course_id), None)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    prereq_ids = course["prerequisites"]
    prereqs = [c for c in MOCK_COURSES if c["id"] in prereq_ids]
    return {"course_id": course_id, "prerequisites": prereqs}