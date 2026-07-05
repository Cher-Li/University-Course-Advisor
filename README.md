# AI Academic Advisor

An AI-powered academic advising platform that helps university students plan their course schedule, check prerequisites, and get personalized degree recommendations.

## Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **AI**: RAG (Chroma, sentence-transformers), Anthropic API
- **Frontend**: React
- **Deployment**: Docker, Render/Railway

## Setup

### Prerequisites

- Python 3.11+
- Docker

### 1. Start the database

```bash
docker run --name advisor-db -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=advisor -p 5433:5432 -d postgres:16
```

If the container already exists but isn't running:

```bash
docker start advisor-db
```

### 2. Set up Python environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

### 4. Seed the database

Creates the tables and populates them with course and prerequisite data:

```bash
python -m app.db.seed
```

### 5. Build the vector store

Embeds course descriptions into Chroma for semantic search:

```bash
python -m app.db.embed
```

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## API Endpoints

| Method | Path                                 | Description                               |
| ------ | ------------------------------------ | ----------------------------------------- |
| GET    | `/health`                            | Health check                              |
| GET    | `/api/v1/courses/`                   | List all courses                          |
| GET    | `/api/v1/courses/{id}`               | Get a course by ID                        |
| GET    | `/api/v1/courses/{id}/prerequisites` | Get prerequisites for a course            |
| POST   | `/api/v1/recommend/`                 | Courses available to take next            |
| POST   | `/api/v1/recommend/missing`          | Missing prerequisites for a target course |
| POST   | `/api/v1/recommend/all-prereqs`      | All prerequisites needed recursively      |
| POST   | `/api/v1/graduation/check`           | Check graduation requirements             |
| GET    | `/api/v1/search?q=`                  | Semantic search over course descriptions  |
| POST   | `/api/v1/search/build`               | Rebuild the vector store                  |

---

## Project Phases

- **Phase 1** (June 15-28): Backend fundamentals, course database API
- **Phase 2** (June 29-July 12): Recommendation logic, prerequisite checking
- **Phase 3** (July 13-26): RAG — embeddings and vector database
- **Phase 4** (July 27-Aug 9): LLM-powered advising
- **Phase 5** (Aug 10-23): React frontend
- **Phase 6** (Aug 24-31): Docker, deployment, polish
