"""
Run this once after seeding the DB to populate the vector store.

Usage:
    python -m app.db.embed
"""

from app.db.session import SessionLocal
from app.services.vector_store import build_vector_store

def main():
    print("Building vector store...")
    db = SessionLocal()
    try:
        build_vector_store(db)
        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()