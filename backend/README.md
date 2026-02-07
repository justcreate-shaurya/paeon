# Paeon AI Backend

## Production-Grade Clinical Intelligence System

This backend powers the Paeon AI Digital Medical Representative platform.

## Quick Start

```bash
# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --port 8000

# Start Celery worker (in separate terminal)
celery -A app.workers.celery_app worker --loglevel=info
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Configuration, security
│   ├── db/            # Database models, sessions
│   ├── services/      # Business logic
│   │   ├── slang/     # Slang-to-Clinical engine
│   │   ├── rag/       # RAG Intelligence system
│   │   ├── assets/    # Fair Balance asset generation
│   │   └── compliance/# Safety & audit services
│   ├── schemas/       # Pydantic models
│   └── workers/       # Celery background tasks
├── alembic/           # Database migrations
├── tests/             # Test suite
└── prompts/           # LLM prompt templates
```

## Compliance

This system adheres to:
- DPDP Act 2023 (India) data protection
- Fair Balance medical content guidelines
- Clinical Decision Support (CDS) regulations

## License

Proprietary - All Rights Reserved
