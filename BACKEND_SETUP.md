# Backend Setup & Verification Guide

## Quick Start — Production Backend

### 1. Create & activate virtual environment
```powershell
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Start the backend server
```powershell
# Run from backend folder
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

---

## Quick Start — Stub Backend (Minimal Testing)

For quick smoke testing without installing all dependencies:

```powershell
# From repo root, using stub (no DB/ML packages required)
uvicorn backend_stub:app --port 9000
```

Stub runs on `http://localhost:9000` with the same API contracts.

---

## Frontend + Backend Integration

### 1. Start Backend
```powershell
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend (in new terminal)
```powershell
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### 3. Verify CORS & API Connectivity
Frontend will automatically call `http://localhost:8000/api/v1/*` endpoints.

Check browser console for any CORS or API errors.

---

## API Endpoints Verified Compatible

### Slang-to-Clinical Translation
- `POST /api/v1/slang/translate` — Translate patient language
- `POST /api/v1/slang/quick-translate` — Quick demo translation
- `GET /api/v1/slang/languages` — Supported languages list
- `POST /api/v1/slang/translations/{id}/feedback` — Clinician feedback

### RAG Intelligence Feed
- `GET /api/v1/rag/intel-feed` — Paginated intelligence feed
- `POST /api/v1/rag/search` — **[FIXED]** Returns wrapped SearchResponse
- `GET /api/v1/rag/verify-source/{id}` — Verify source citations
- `GET /api/v1/rag/drug/{drug_name}` — Get drug info & recent intelligence

### Asset Generation
- `POST /api/v1/assets/generate` — Generate patient education asset
- `GET /api/v1/assets/{asset_id}` — Retrieve asset
- `POST /api/v1/assets/export/pdf` — Export as PDF
- `POST /api/v1/assets/export/png` — Export as PNG
- `POST /api/v1/assets/quick-generate` — Demo asset generation
- `GET /api/v1/assets/drugs/available` — List available drugs

### Health & Compliance
- `GET /api/v1/health` — System health check
- `GET /api/v1/compliance` — Compliance status

---

## Known Issues & Fixes Applied

### Issue: `/rag/search` response mismatch
- **Problem**: Frontend expected `SearchResponse { results[], query, total }` but backend returned raw `list[IntelligenceItem]`
- **Fixed**: Updated backend to return wrapped response; frontend normalized to handle both formats

### Issue: Heavy dependencies blocking startup
- **Solution**: Use stub backend for quick testing, or install all dependencies from `requirements.txt`

---

## Troubleshooting

### Port already in use
```powershell
# Use different port
uvicorn app.main:app --port 8001
# Then update frontend VITE_API_URL=http://localhost:8001/api/v1
```

### Missing Python packages during startup
1. Check `requirements.txt` is installed: `pip list | grep fastapi`
2. Install from backend folder: `cd backend && pip install -r requirements.txt`
3. For optional ML packages: uncomment in `requirements.txt` and reinstall

### CORS errors in browser
- Ensure backend runs at `http://localhost:8000` (default)
- Check `backend/app/core/config.py` has `cors_origins` including `http://localhost:5173`

---

## Files Modified for FE/BE Compatibility

1. **src/lib/api.ts** — Normalized `ragApi.search()` response handling
2. **backend/app/schemas/__init__.py** — Added `SearchResult` and `SearchResponse` models
3. **backend/app/api/rag.py** — Updated `/rag/search` to return `SearchResponse` wrapper
4. **backend_stub.py** — Created minimal stub for quick testing
5. **backend/requirements.txt** — Extracted core dependencies from pyproject.toml
