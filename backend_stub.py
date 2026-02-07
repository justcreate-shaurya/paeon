from fastapi import FastAPI, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 5
    include_sources: Optional[List[str]] = None


@app.post("/api/v1/rag/search")
def rag_search(req: SearchRequest):
    # Return a consistent wrapper the frontend expects
    results = [
        {
            "title": f"Demo result for {req.query}",
            "content": "This is a demo search result.",
            "confidence": 0.91,
            "source": "demo",
            "drug_name": "DemoDrug",
            "url": "https://example.com/demo"
        }
        for _ in range(min(req.limit or 1, 3))
    ]
    return {"results": results}


class SlangRequest(BaseModel):
    text: str


@app.post("/api/v1/slang/translate")
def slang_translate(req: SlangRequest):
    return {
        "id": "demo-1",
        "raw_input": req.text,
        "original_language": "en",
        "clinical_interpretation": "Demo clinical interpretation",
        "confidence": 0.9,
        "standard_codes": [],
        "rationale": "Auto-generated demo"
    }


class GenerateRequest(BaseModel):
    drug_name: str
    asset_type: str
    target_audience: Optional[str] = "patient"
    language: Optional[str] = "en"
    include_fair_balance: Optional[bool] = True


@app.post("/api/v1/assets/generate")
def assets_generate(req: GenerateRequest):
    asset = {
        "id": "demo-asset",
        "drug_name": req.drug_name,
        "strength": "500mg Tablet",
        "asset_type": req.asset_type,
        "content": {
            "title": req.drug_name,
            "dosage_instruction": "Take with meals, twice daily.",
            "benefits": ["Benefit 1", "Benefit 2"],
            "fair_balance": "Demo fair balance text",
            "footer_text": "Consult your healthcare provider"
        },
        "compliance_status": "approved",
        "compliance_score": 0.95
    }
    return asset


@app.post("/api/v1/assets/export/{format}")
def assets_export(format: str, payload: dict = Body(...)):
    # Return a small PDF/PNG bytes placeholder
    if format == "pdf":
        data = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        return Response(content=data, media_type="application/pdf")
    else:
        data = b"PNGDATA"
        return Response(content=data, media_type="image/png")
