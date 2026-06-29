"""
Graduation rule checking.

Checks whether a student is on track to graduate based on:
- Required core courses
- Minimum total credits
- Minimum upper-level credits (300+)
- Minimum elective credits

Hardcoded for now
"""

from dataclasses import dataclass

# requirements
REQUIRED_CORE_COURSES = [
    "COMP250",  # Intro to CS
    "MATH240",  # Discrete Structures
    "COMP302",  # Programming Languages
    "COMP330",  # Theory of Computation
]

MIN_TOTAL_CREDITS = 120
MIN_UPPER_LEVEL_CREDITS = 30  # 300-level and above
MIN_CS_ELECTIVE_CREDITS = 15  # any CS course beyond core

# Credits per course (will come from DB in a later phase)
COURSE_CREDITS: dict[str, int] = {
    "COMP250": 3,
    "MATH240": 3,
    "COMP302": 3,
    "COMP330": 3,
    "COMP424": 3,
    "COMP551": 4,
}


@dataclass
class GraduationRequirement:
    name: str
    satisfied: bool
    detail: str


@dataclass
class GraduationReport:
    can_graduate: bool
    requirements: list[GraduationRequirement]

    def to_dict(self) -> dict:
        return {
            "can_graduate": self.can_graduate,
            "requirements": [
                {
                    "name": r.name,
                    "satisfied": r.satisfied,
                    "detail": r.detail,
                }
                for r in self.requirements
            ],
        }


# Checker
def check_graduation(completed: set[str]) -> GraduationReport:
    """
    Given a set of completed course IDs, return a graduation report
    detailing which requirements are met and which are not.
    """
    requirements = []

    # 1. Core courses
    missing_core = [c for c in REQUIRED_CORE_COURSES if c not in completed]
    requirements.append(GraduationRequirement(
        name="Core courses",
        satisfied=len(missing_core) == 0,
        detail=(
            "All core courses completed."
            if not missing_core
            else f"Missing: {', '.join(missing_core)}"
        ),
    ))

    # 2. Total credits
    total_credits = sum(COURSE_CREDITS.get(c, 3) for c in completed)
    requirements.append(GraduationRequirement(
        name="Total credits",
        satisfied=total_credits >= MIN_TOTAL_CREDITS,
        detail=f"{total_credits} / {MIN_TOTAL_CREDITS} credits completed.",
    ))

    # 3. Upper-level credits (300+)
    upper_level = {c for c in completed if _is_upper_level(c)}
    upper_credits = sum(COURSE_CREDITS.get(c, 3) for c in upper_level)
    requirements.append(GraduationRequirement(
        name="Upper-level credits",
        satisfied=upper_credits >= MIN_UPPER_LEVEL_CREDITS,
        detail=f"{upper_credits} / {MIN_UPPER_LEVEL_CREDITS} upper-level credits completed.",
    ))

    # 4. CS elective credits (any CS course beyond core)
    electives = {
        c for c in completed
        if c.startswith("COMP") and c not in REQUIRED_CORE_COURSES
    }
    elective_credits = sum(COURSE_CREDITS.get(c, 3) for c in electives)
    requirements.append(GraduationRequirement(
        name="CS elective credits",
        satisfied=elective_credits >= MIN_CS_ELECTIVE_CREDITS,
        detail=f"{elective_credits} / {MIN_CS_ELECTIVE_CREDITS} elective credits completed.",
    ))

    can_graduate = all(r.satisfied for r in requirements)
    return GraduationReport(can_graduate=can_graduate, requirements=requirements)


def _is_upper_level(course_id: str) -> bool:
    """Return True if the course is 300-level or above."""
    for char in course_id:
        if char.isdigit():
            return int(char) >= 3
    return False