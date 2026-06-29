"""
Graduation checking endpoints.

POST /graduation/check  -> given completed courses, on track to graduate?
"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.graduation import check_graduation

router = APIRouter(prefix="/graduation", tags=["graduation"])

class CompletedCoursesInput(BaseModel):
    completed: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"completed": ["COMP250", "MATH240", "COMP302", "COMP330", "COMP424"]}
            ]
        }
    }

@router.post("/check")
def check(body: CompletedCoursesInput):
    """
    Given a list of completed course IDs, return a graduation report
    showing which requirements are met and which are not.
    """
    report = check_graduation(set(body.completed))
    return report.to_dict()