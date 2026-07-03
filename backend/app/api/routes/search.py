"""
Semantic search endpoints.

GET  /search?q=machine learning -> find relevant courses by description
POST /search/build -> rebuild the vector store from DB
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.vector_store import search_courses, build_vector_store

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def search(q: str = Query(..., description="Natural language search query"), n: int = 3):
    """
    Semantic search over course descriptions.
    Example: /api/v1/search?q=computer vision and image processing
    """
    results = search_courses(q, n_results=n)
    return {"query": q, "results": results}


@router.post("/build")
def build(db: Session = Depends(get_db)):
    """Rebuild the vector store from the current course database."""
    build_vector_store(db)
    return {"status": "ok"}