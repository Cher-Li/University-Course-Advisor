"""
Vector store service.

Embeds course descriptions using sentence-transformers and stores
them in a local Chroma collection for semantic search.

Usage:
    from app.services.vector_store import build_vector_store, search_courses

    build_vector_store(db)  # run once to populate
    results = search_courses("machine learning and neural networks")
"""

import chromadb
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from app.models.course import Course

# Local Chroma DB persisted to disk
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "courses"
MODEL_NAME = "all-MiniLM-L6-v2"

_client = None
_collection = None
_model = None

def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def _get_collection():
    global _collection
    if _collection is None:
        _collection = _get_client().get_or_create_collection(COLLECTION_NAME)
    return _collection


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def build_vector_store(db: Session) -> None:
    """
    Load all courses from the DB, embed their descriptions,
    and store them in Chroma. Safe to re-run — skips existing entries.
    """
    courses = db.query(Course).all()
    collection = _get_collection()
    model = _get_model()

    existing = set(collection.get()["ids"])

    new_courses = [c for c in courses if c.id not in existing]
    if not new_courses:
        print("Vector store already up to date.")
        return

    docs = [f"{c.name}. {c.description or ''}" for c in new_courses]
    ids = [c.id for c in new_courses]
    metadatas = [{"name": c.name, "credits": c.credits} for c in new_courses]

    embeddings = model.encode(docs).tolist()

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"Added {len(new_courses)} courses to vector store.")


def search_courses(query: str, n_results: int = 3) -> list[dict]:
    """
    Semantic search over course descriptions.
    Returns the top n_results most relevant courses.

    Example:
        search_courses("neural networks and deep learning")
        -> [{"id": "COMP551", "name": "Applied Machine Learning", ...}, ...]
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    courses = []
    for i, course_id in enumerate(results["ids"][0]):
        courses.append({
            "id": course_id,
            "name": results["metadatas"][0][i]["name"],
            "credits": results["metadatas"][0][i]["credits"],
            "description": results["documents"][0][i],
            "relevance_score": round(1 - results["distances"][0][i], 3),
        })

    return courses