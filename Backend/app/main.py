from fastapi import FastAPI
from app.api.routes import courses, recommend
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
)

app.include_router(courses.router, prefix="/api/v1")

app.include_router(recommend.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"} 