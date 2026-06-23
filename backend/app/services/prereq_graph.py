"""
Each course is a node. 
Directed edge A -> B means "A is a prerequisite of B"

Currently mock data
"""

from typing import Optional


# Adjacency list: course_id -> list of prerequisite course_ids

# Mock data
PREREQ_MAP: dict[str, list[str]] = {
    "COMP250": [],
    "MATH240": [],
    "COMP302": ["COMP250"],
    "COMP330": ["COMP250", "MATH240"],
    "COMP424": ["COMP302"], 
    "COMP551": ["COMP302", "MATH240"], 
}

def can_take(course_id: str, completed: set[str]) -> bool:
    """
    Return True if all prerequisites for course_id are in completed.

    Example:
        can_take("COMP302", {"COMP250"})  -> True
        can_take("COMP330", {"COMP250"})  -> False (missing MATH240)
    """
    prereqs = PREREQ_MAP.get(course_id, [])
    return all(p in completed for p in prereqs)

def missing_prereqs(course_id: str, completed: set[str]) -> list[str]:
    """
    Return the list of prerequisites still needed for course_id.

    Example:
        missing_prereqs("COMP330", {"COMP250"})  -> ["MATH240"]
    """
    prereqs = PREREQ_MAP.get(course_id, [])
    return [p for p in prereqs if p not in completed]

def available_courses(completed: set[str]) -> list[str]:
    """
    Return all courses whose prerequisites are fully satisfied
    but that haven't been completed yet.

    Example:
        available_courses({"COMP250", "MATH240"})
        -> ["COMP302", "COMP330"]
    """
    return [
        course_id
        for course_id in PREREQ_MAP
        if course_id not in completed and can_take(course_id, completed)
    ]

def all_prerequisites(course_id: str, visited: Optional[set[str]] = None) -> set[str]:
    """
    Recursively find ALL prerequisites for a course, not just direct ones.
    Useful for answering "what do I need to eventually take COMP551?"

    Example:
        all_prerequisites("COMP551")
        -> {"COMP302", "COMP250", "MATH240"}
    """
    if visited is None:
        visited = set()

    direct = PREREQ_MAP.get(course_id, [])
    for prereq in direct:
        if prereq not in visited:
            visited.add(prereq)
            all_prerequisites(prereq, visited)

    return visited