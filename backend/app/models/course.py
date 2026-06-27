"""
Database models.

Two tables:
- courses        stores course info (id, name, credits, description)
- prerequisites  join table storing edges in the prereq graph
                 e.g. (course_id=COMP302, prereq_id=COMP250)
                 means COMP250 is required before COMP302
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True) 
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False, default=3)
    description = Column(Text, nullable=True)

    prerequisites = relationship(
        "Prerequisite",
        foreign_keys="Prerequisite.course_id",
        back_populates="course",
    )

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    course_id = Column(String, ForeignKey("courses.id"), primary_key=True)
    prereq_id = Column(String, ForeignKey("courses.id"), primary_key=True)

    course = relationship("Course", foreign_keys=[course_id], back_populates="prerequisites")
    prereq = relationship("Course", foreign_keys=[prereq_id])