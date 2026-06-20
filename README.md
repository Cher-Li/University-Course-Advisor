# AI Academic Advisor

An AI-powered academic advising platform that helps university students plan their course schedule, check prerequisites, and get personalized degree recommendations.

## Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **AI**: RAG (Chroma/FAISS), Anthropic API
- **Frontend**: React
- **Deployment**: Docker, Render/Railway

## Setup

### Prerequisites

- Python 3.11+
- Docker <- wip

### Backend <- wip

```bash
# Start local Postgres
docker run --name advisor-db -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=advisor -p 5432:5432 -d postgres:16

# Set up Python env
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure env
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

| Method | Path                                 | Description                    |
| ------ | ------------------------------------ | ------------------------------ |
| GET    | `/health`                            | Health check                   |
| GET    | `/api/v1/courses/`                   | List all courses               |
| GET    | `/api/v1/courses/{id}`               | Get a course by ID             |
| GET    | `/api/v1/courses/{id}/prerequisites` | Get prerequisites for a course |

## Project Phases

- **Phase 1** (June 15-28): Backend fundamentals, course database API
- **Phase 2** (June 29-July 12): Recommendation logic, prerequisite checking
- **Phase 3** (July 13-26): RAG — embeddings and vector database
- **Phase 4** (July 27-Aug 9): LLM-powered advising
- **Phase 5** (Aug 10-23): React frontend
- **Phase 6** (Aug 24-31): Docker, deployment, polish
