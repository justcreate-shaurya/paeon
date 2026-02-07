# Paeon AI - Production Setup Guide

This guide explains how to enable AI features and move from the stub backend to the full production system.

## Current State

**Frontend:** ✅ Running (Vite dev server at http://localhost:5173)
**Backend:** ⚠️ Running stub only (minimal mock API at http://127.0.0.1:8000)

The stub provides:
- `/api/v1/health` — health check
- `/api/v1/rag/search` — returns mock search results
- `/api/v1/slang/translate` — returns mock translations
- `/api/v1/assets/generate` — returns mock asset data
- `/api/v1/assets/export/{format}` — returns mock file download

---

## What You Need for Full AI Features

### 1. **Large Language Model (LLM) Integration**

For features like slang translation, asset generation, and patient communication:

#### Option A: OpenAI API (Recommended for MVP)
```bash
pip install openai
```

**Setup:**
- Create account at https://platform.openai.com
- Generate API key in account settings
- Add to `backend/.env`:
  ```
  OPENAI_API_KEY=sk-xxx...
  OPENAI_MODEL=gpt-4-turbo-preview
  ```

**Backend code example** (in `backend/app/services/slang/engine.py`):
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "system",
            "content": "You are a medical translator. Convert patient vernacular to clinical terminology.",
            "role": "user",
            "content": f"Translate: {text}"
        }]
    )
    return parse_response(response.choices[0].message.content)
```

#### Option B: Open Source LLM (Ollama)
```bash
# Install Ollama from https://ollama.ai
ollama pull mistral  # or llama2, neural-chat, etc.
ollama serve  # runs on localhost:11434
```

Then use `ollama` Python client.

---

### 2. **Vector Database for RAG (Retrieval-Augmented Generation)**

Qdrant for semantic search over medical documents:

```bash
pip install qdrant-client
```

**Setup Qdrant:**

Option A: Docker (Recommended)
```bash
docker run -p 6333:6333 \
  -e QDRANT_API_KEY=your-api-key \
  qdrant/qdrant:latest
```

Option B: Python in-memory (for testing)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")  # or ":6333" for server
client.recreate_collection(
    collection_name="medical_docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
```

**Backend code example** (in `backend/app/services/rag/engine.py`):
```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

embeddings = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = QdrantClient(url="http://localhost:6333")

def index_documents(docs: list[str]):
    vectors = embeddings.encode(docs)
    client.upsert(
        collection_name="medical_docs",
        points=[{
            "id": i,
            "vector": vec,
            "payload": {"text": doc}
        } for i, (vec, doc) in enumerate(zip(vectors, docs))]
    )

def search(query: str, limit: int = 5):
    query_vec = embeddings.encode([query])[0]
    results = client.search(
        collection_name="medical_docs",
        query_vector=query_vec.tolist(),
        limit=limit
    )
    return [hit.payload["text"] for hit in results]
```

---

### 3. **Database (PostgreSQL with AsyncPG)**

Already in requirements.txt. Setup:

```bash
# Docker
docker run -e POSTGRES_PASSWORD=paeon -e POSTGRES_DB=paeon_db \
  -p 5432:5432 postgres:15

# Or local PostgreSQL
brew install postgresql  # macOS
# Windows: use installer
```

**Add to `backend/.env`:**
```
DATABASE_URL=postgresql+asyncpg://postgres:paeon@localhost:5432/paeon_db
```

**Backend code** (already in `backend/app/db/models.py`):
```python
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Translation(Base):
    __tablename__ = "translations"
    id = Column(String, primary_key=True)
    raw_input = Column(String)
    clinical_interpretation = Column(String)
    confidence = Column(Float)
```

---

### 4. **Redis (for Caching & Task Queue)**

For async tasks and session management:

```bash
docker run -p 6379:6379 redis:7-alpine
```

**Add to `backend/.env`:**
```
REDIS_URL=redis://localhost:6379
```

**Backend code example** (in services):
```python
import redis
from celery import Celery

redis_client = redis.Redis(host='localhost', port=6379)
celery_app = Celery(broker='redis://localhost:6379')

@celery_app.task
def generate_asset_async(drug_name: str):
    # Long-running LLM generation
    return llm_generate_patient_card(drug_name)
```

---

### 5. **Data Sources (Medical APIs)**

Populate your RAG database with real medical data:

#### FDA MedWatch API
```python
import requests

def fetch_fda_recalls():
    response = requests.get(
        "https://api.fda.gov/drug/event.json",
        params={"search": "serious:true", "limit": 100}
    )
    return response.json()["results"]
```

#### PubMed API
```python
import requests

def fetch_pubmed_papers(drug: str):
    response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params={"db": "pubmed", "term": drug, "retmax": 50}
    )
    return response.text
```

#### DailyMed
```python
# Use beautifulsoup to scrape DailyMed clinical documents
from bs4 import BeautifulSoup

def fetch_dailymed(drug_name: str):
    # Search DailyMed, extract structured label data
```

---

### 6. **NLP & Biomedical Models**

For slang interpretation and concept extraction:

```bash
pip install spacy scispacy sentence-transformers langdetect
python -m spacy download en_core_sci_md
```

**Backend code:**
```python
import spacy
from scispacy.linking import EntityLinker

nlp = spacy.load("en_core_sci_md")
nlp.add_pipe("scispacy_linker")

def extract_medical_entities(text: str):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities
```

---

## Full Backend Setup (From Stub → Production)

### Step 1: Install Full Requirements
```bash
cd backend
python -m venv venv_prod
source venv_prod/bin/activate  # Windows: venv_prod\Scripts\Activate
pip install -r requirements.txt
```

### Step 2: Start Services (Docker Compose)

Create `docker-compose.yml`:
```yaml
version: '3.9'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: paeon
      POSTGRES_DB: paeon_db
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"

  backend:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:paeon@postgres:5432/paeon_db
      REDIS_URL: redis://redis:6379
      QDRANT_URL: http://qdrant:6333
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
      - qdrant

  frontend:
    working_dir: /app
    command: npm run dev
    ports:
      - "5173:5173"
    volumes:
      - .:/app
```

Run:
```bash
docker-compose up
```

### Step 3: Run Database Migrations
```bash
alembic upgrade head
```

### Step 4: Seed RAG Data
```python
# backend/scripts/seed_rag.py
from app.services.rag.engine import index_fda_recalls, index_pubmed_papers

if __name__ == "__main__":
    print("Fetching FDA recalls...")
    recalls = fetch_fda_recalls()
    index_fda_recalls(recalls)
    
    print("Fetching PubMed papers...")
    papers = fetch_pubmed_papers("diabetes medication")
    index_pubmed_papers(papers)
```

Run:
```bash
python backend/scripts/seed_rag.py
```

---

## Environment Variables Checklist

Create `backend/.env`:
```
# LLM
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=postgresql+asyncpg://postgres:paeon@localhost:5432/paeon_db
REDIS_URL=redis://localhost:6379

# RAG
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-key

# App
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Data Sources
FDA_API_KEY=your-key  # if required
PUBMED_API_KEY=your-key  # if required
```

---

## Quick Start: From Here

**Next steps to go live:**

1. ✅ Frontend working (you're here!)
2. Get OpenAI API key → add to `backend/.env`
3. Start Docker services: `docker-compose up`
4. Test endpoints: `curl http://localhost:8000/api/v1/slang/translate`
5. Seed medical data: `python backend/scripts/seed_rag.py`
6. Update `VITE_API_URL=http://localhost:8000` in frontend `.env`
7. Test end-to-end slang → clinical translation

---

## Cost Estimates (Monthly)

| Service | Free Tier | Paid |
|---------|-----------|------|
| OpenAI GPT-4 | — | $10-50 (depends on usage) |
| Qdrant (self-hosted) | ✅ Docker | AWS/Azure hosting |
| PostgreSQL (AWS RDS) | 12 months free | ~$15-30 |
| Redis | Docker free | ~$10-15 |
| **Total** | **~$0** (self-hosted) | **~$50-100** (cloud) |

---

## Troubleshooting

**Q: "LLM request timeout"**
- Check OpenAI API key is valid
- Ensure network can reach api.openai.com
- Increase timeout in `backend/app/core/config.py`

**Q: "Qdrant connection refused"**
- Verify Qdrant is running: `curl http://localhost:6333/health`
- Check `QDRANT_URL` in `.env`

**Q: "Database migration error"**
- Drop & recreate: `psql -c "DROP DATABASE paeon_db; CREATE DATABASE paeon_db;"`
- Rerun: `alembic upgrade head`

---

**Status:** You now have a working frontend with mock data. Enabling real AI requires LLM + vector DB + real data sources. Start with OpenAI API key + Qdrant for MVP.
