"""
Recommendation endpoints.

POST /recommend -> given completed courses, what to take next?
POST /recommend/missing -> given a target course, what prereqs missing?
POST /recommend/all-prereqs -> all prerequisites needed for a course
"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.prereq_graph import (
    available_courses,
    missing_prereqs,
    all_prerequisites,
)

router = APIRouter(prefix="/recommend", tags=["recommendations"])

class CompletedCoursesInput(BaseModel):
    completed: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [{"completed": ["COMP250", "MATH240"]}]
        }
    }

class TargetCourseInput(BaseModel):
    target: str
    completed: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [{"target": "COMP330", "completed": ["COMP250"]}]
        }
    }

@router.post("/")
def recommend(body: CompletedCoursesInput):
    """
    Given a list of completed courses, return everything the student
    is now eligible to take.
    """
    available = available_courses(set(body.completed))
    return {
        "completed": body.completed,
        "available": available,
    }

@router.post("/missing")
def missing(body: TargetCourseInput):
    """
    Given a target course and completed courses, return what
    prerequisites are still needed.
    """
    missing = missing_prereqs(body.target, set(body.completed))
    return {
        "target": body.target,
        "completed": body.completed,
        "missing_prerequisites": missing,
        "can_take": len(missing) == 0,
    }

@router.post("/all-prereqs")
def all_prereqs(body: TargetCourseInput):
    """
    Recursively find every course needed to eventually take the target,
    regardless of how many levels deep.
    """
    all_prereqs = all_prerequisites(body.target)
    still_needed = all_prereqs - set(body.completed)
    return {
        "target": body.target,
        "all_prerequisites": sorted(all_prereqs),
        "still_needed": sorted(still_needed),
    }