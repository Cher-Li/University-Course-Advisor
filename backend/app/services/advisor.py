"""
LLM-powered advisor service.

Takes a student's goal, completed courses, and retrieves relevant
context before passing everything to an LLM to generate advice.

Flow:
    1. Semantic search for relevant courses (RAG)
    2. Check what courses are available to take (prereq graph)
    3. Build a prompt with all context
    4. Call LLM like Claude and return the response
"""

import anthropic
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.vector_store import search_courses
from app.services.prereq_graph import available_courses

USE_MOCK = True

def get_advice(goal: str, completed: list[str], db: Session) -> str:
    """
    Given a student's goal and completed courses, return LLM-generated advice.

    Example:
        get_advice("I want ML internships", ["COMP250", "MATH240"], db)
        -> "Based on your background, I recommend COMP551 next because..."
    """

    # Step 1: Retrieve semantically relevant courses
    relevant_courses = search_courses(goal, n_results=5)

    # Step 2: Get courses the student is eligible to take
    available = available_courses(set(completed), db)

    # Step 3: Build context for the prompt
    relevant_text = "\n".join(
        f"- {c['id']}: {c['name']} — {c['description']} (relevance: {c['relevance_score']})"
        for c in relevant_courses
    )

    available_text = ", ".join(available) if available else "None at this time"
    completed_text = ", ".join(completed) if completed else "None"

    if USE_MOCK:
        return _mock_response(goal, completed_text, available_text, relevant_text)


    # Step 4: Call Claude
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = f"""You are an AI academic advisor for a university CS student.

    The student's goal: {goal}

    Courses they have already completed:
    {completed_text}

    Courses they are currently eligible to take (prerequisites satisfied):
    {available_text}

    Courses most relevant to their goal (from semantic search):
    {relevant_text}

    Please give the student clear, specific advice on:
    1. Which courses to prioritize and why
    2. What the ideal order is if there are dependencies
    3. Any gaps between their current standing and their goal
    4. A suggested plan for the next 1-2 semesters

    Be concise, practical, and encouraging. Reference specific course IDs where helpful."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def _mock_response(goal, completed_text, available_text, relevant_text) -> str:
    return f"""[MOCK RESPONSE]
 
    Based on your goal "{goal}", here's my advice:
    
    Completed courses: {completed_text}
    Currently available to you: {available_text}
    
    Most relevant courses for your goal:
    {relevant_text}
    
    Recommended plan:
    - Next semester: prioritize the highest-relevance courses listed above that you're eligible for
    - Make sure prerequisites are cleared early so upper-level courses open up
    - Aim to have core requirements done by the end of next semester
    
    Once the real LLM is connected, this will be a fully personalized response based on your specific situation.
    """
