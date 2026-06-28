"""
Each course is a node. 
Directed edge A -> B means "A is a prerequisite of B"

Now builds based on DB rows
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.course import Prerequisite


# Adjacency list: course_id -> list of prerequisite course_ids

def build_prereq_map(db: Session) -> dict[str, list[str]]:
    """Load all prerequisite edges from the DB into an adjacency list."""
    rows = db.query(Prerequisite).all()
    prereq_map: dict[str, list[str]] = {}
    for row in rows:
        prereq_map.setdefault(row.course_id, []).append(row.prereq_id)
    return prereq_map


def can_take(course_id: str, completed: set[str], db: Session) -> bool:
    """
    Return True if all prerequisites for course_id are in completed.

    Example:
        can_take("COMP302", {"COMP250"})  -> True
        can_take("COMP330", {"COMP250"})  -> False (missing MATH240)
    """
    prereq_map = build_prereq_map(db)
    prereqs = prereq_map.get(course_id, [])
    return all(p in completed for p in prereqs)

def missing_prereqs(course_id: str, completed: set[str], db: Session) -> list[str]:
    """
    Return the list of prerequisites still needed for course_id.

    Example:
        missing_prereqs("COMP330", {"COMP250"})  -> ["MATH240"]
    """
    prereq_map = build_prereq_map(db)
    prereqs = prereq_map.get(course_id, [])
    return [p for p in prereqs if p not in completed]

def available_courses(completed: set[str], db: Session) -> list[str]:
    """
    Return all courses whose prerequisites are fully satisfied
    but that haven't been completed yet.

    Example:
        available_courses({"COMP250", "MATH240"})
        -> ["COMP302", "COMP330"]
    """
    prereq_map = build_prereq_map(db)
    return [
        course_id
        for course_id, prereqs in prereq_map.items()
        if course_id not in completed and all(p in completed for p in prereqs)
    ]

def all_prerequisites(course_id: str, db: Session, visited: Optional[set[str]] = None) -> set[str]:
    """
    Recursively find ALL prerequisites for a course, not just direct ones.
    Useful for answering "what do I need to eventually take COMP551?"

    Example:
        all_prerequisites("COMP551")
        -> {"COMP302", "COMP250", "MATH240"}
    """
    if visited is None:
        visited = set()

    prereq_map = build_prereq_map(db)
    direct = prereq_map.get(course_id, [])
    for prereq in direct:
        if prereq not in visited:
            visited.add(prereq)
            all_prerequisites(prereq, db, visited)
 
    return visited