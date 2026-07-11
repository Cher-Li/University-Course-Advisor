"""
LLM advising endpoint.

POST /advise  -> given a goal and completed courses, get AI-generated advice
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.advisor import get_advice

router = APIRouter(prefix="/advise", tags=["advisor"])

class AdviceRequest(BaseModel):
    goal: str
    completed: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "goal": "I want to get an ML internship",
                    "completed": ["COMP250", "MATH240"],
                }
            ]
        }
    }

@router.post("/")
def advise(body: AdviceRequest, db: Session = Depends(get_db)):
    """
    Get personalized AI advice based on your goal and completed courses.
    """
    advice = get_advice(body.goal, body.completed, db)
    return {
        "goal": body.goal,
        "completed": body.completed,
        "advice": advice,
    } 