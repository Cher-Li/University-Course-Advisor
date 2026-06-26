"""
Run this once to create tables and populate with seed data.

Usage:
    python -m app.db.seed
"""

from app.db.session import engine, SessionLocal, Base
from app.models.course import Course, Prerequisite # add this next

COURSES = [
    {"id": "COMP250", "name": "Intro to Computer Science", "credits": 3, "description": "Foundations of CS: data structures, algorithms, and complexity."},
    {"id": "MATH240", "name": "Discrete Structures", "credits": 3, "description": "Logic, sets, graph theory, and combinatorics."},
    {"id": "COMP302", "name": "Programming Languages and Paradigms", "credits": 3, "description": "Functional and imperative programming, type systems, interpreters."},
    {"id": "COMP330", "name": "Theory of Computation", "credits": 3, "description": "Automata, formal languages, and computability."},
    {"id": "COMP424", "name": "Artificial Intelligence", "credits": 3, "description": "Search, knowledge representation, planning, and machine learning basics."},
    {"id": "COMP551", "name": "Applied Machine Learning", "credits": 4, "description": "Supervised and unsupervised learning, neural networks, and evaluation."},
]

PREREQUISITES = [
    {"course_id": "COMP302", "prereq_id": "COMP250"},
    {"course_id": "COMP330", "prereq_id": "COMP250"},
    {"course_id": "COMP330", "prereq_id": "MATH240"},
    {"course_id": "COMP424", "prereq_id": "COMP302"},
    {"course_id": "COMP551", "prereq_id": "COMP302"},
    {"course_id": "COMP551", "prereq_id": "MATH240"},
]

def seed():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Skip if already seeded
        if db.query(Course).first():
            print("Database already seeded, skipping.")
            return

        print("Seeding courses...")
        for c in COURSES:
            db.add(Course(**c))
        db.commit()

        print("Seeding prerequisites...")
        for p in PREREQUISITES:
            db.add(Prerequisite(**p))
        db.commit()

        print("Done.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()