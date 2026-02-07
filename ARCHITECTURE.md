# Paeon AI - System Architecture

## Overview

Paeon AI is a **regulated clinical intelligence system** that serves as a Digital Medical Representative (DMR). It bridges the gap between colloquial patient language and structured clinical terminology while providing real-time regulatory intelligence and compliant patient education materials.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    PAEON AI PLATFORM                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                           PRESENTATION LAYER (React)                              │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────────────┐   │    │
│  │  │ Slang-to-Clinical│  │ Intelligence Feed│  │     Live Asset Preview        │   │    │
│  │  │    Translator    │  │                  │  │   (Patient Education Card)    │   │    │
│  │  │  • Input Panel   │  │  • FDA Recalls   │  │   • Drug Info                 │   │    │
│  │  │  • Translation   │  │  • Indications   │  │   • Usage Instructions        │   │    │
│  │  │  • Confidence    │  │  • Safety Alerts │  │   • Benefits/Risks            │   │    │
│  │  │  • Clinician Edit│  │  • Source Verify │  │   • Export PDF/PNG            │   │    │
│  │  └──────────────────┘  └──────────────────┘  └───────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                           │                                              │
│                                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                              API GATEWAY (FastAPI)                                │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌────────────────────────┐  │    │
│  │  │   /slang/   │  │   /rag/      │  │  /assets/   │  │      /export/          │  │    │
│  │  │  translate  │  │  intel-feed  │  │   generate  │  │        pdf             │  │    │
│  │  └─────────────┘  └──────────────┘  └─────────────┘  └────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                           │                                              │
│                                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                           COMPLIANCE & SAFETY LAYER                               │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────────────────┐  │    │
│  │  │ PII Stripper │  │Safety Validator│ │Audit Logger│  │ Fair Balance Checker  │  │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  └───────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                           │                                              │
│                                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                              AI ORCHESTRATION LAYER                               │    │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │                        SLANG-TO-CLINICAL ENGINE                              │  │    │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐   │  │    │
│  │  │  │  Language    │  │  Linguistic  │  │ Semantic   │  │   Clinical       │   │  │    │
│  │  │  │  Detection   │  │  Adapter LLM │  │ Normalizer │  │   Mapper         │   │  │    │
│  │  │  └──────────────┘  └──────────────┘  └────────────┘  └──────────────────┘   │  │    │
│  │  └────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                    │    │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │                        RAG INTELLIGENCE ENGINE                               │  │    │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐   │  │    │
│  │  │  │  Document    │  │   Vector     │  │   BM25     │  │    Source        │   │  │    │
│  │  │  │  Ingester    │  │   Search     │  │   Search   │  │    Reranker      │   │  │    │
│  │  │  └──────────────┘  └──────────────┘  └────────────┘  └──────────────────┘   │  │    │
│  │  └────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                    │    │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │                        FAIR BALANCE ENGINE                                   │  │    │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐   │  │    │
│  │  │  │  Asset       │  │  Benefit/Risk│  │ Compliance │  │   PDF/PNG        │   │  │    │
│  │  │  │  Generator   │  │  Balancer    │  │ Validator  │  │   Exporter       │   │  │    │
│  │  │  └──────────────┘  └──────────────┘  └────────────┘  └──────────────────┘   │  │    │
│  │  └────────────────────────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                           │                                              │
│                                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                              DATA & KNOWLEDGE LAYER                               │    │
│  │  ┌──────────────────┐  ┌───────────────────┐  ┌─────────────────────────────┐   │    │
│  │  │   PostgreSQL     │  │   Vector Store    │  │     External Sources        │   │    │
│  │  │  • Queries       │  │   (Qdrant/Pine)   │  │  • FDA OpenAPI              │   │    │
│  │  │  • Translations  │  │  • FDA Embeddings │  │  • DailyMed                 │   │    │
│  │  │  • Audit Logs    │  │  • PubMed Index   │  │  • PubMed                   │   │    │
│  │  │  • Assets        │  │  • Drug Labels    │  │  • DrugBank                 │   │    │
│  │  │  • Drug Intel    │  │                   │  │                             │   │    │
│  │  └──────────────────┘  └───────────────────┘  └─────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Slang-to-Clinical Translation Flow

```
Patient Input (Any Language)
         │
         ▼
┌────────────────────┐
│  PII Stripper      │ ← Removes personal identifiable information
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Language Detection │ ← Detects source language (100+ languages)
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Linguistic Adapter │ ← LLM translates to English canonical form
│      (LLM)         │   WITHOUT medical interpretation
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Semantic Normalizer│ ← Maps to standardized symptom vocabulary
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Medical Knowledge  │ ← SNOMED-CT / UMLS / ICD concept lookup
│ Graph (KG) Lookup  │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Confidence Scorer  │ ← Calculates mapping confidence (0.0-1.0)
└────────────────────┘
         │
         ▼
┌────────────────────┐
│  Safety Validator  │ ← Ensures no diagnosis/prescription
└────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│ Clinical Translation Output                              │
│ {                                                        │
│   "original_language": "Hindi",                          │
│   "raw_input": "mere seene mein ajeeb sa dard",         │
│   "normalized_english": "strange pain in chest",         │
│   "clinical_interpretation": "Atypical Chest Pain",     │
│   "standard_codes": [                                    │
│     { "system": "SNOMED-CT", "code": "29857009" },      │
│     { "system": "ICD-10", "code": "R07.9" }             │
│   ],                                                     │
│   "confidence": 0.87,                                    │
│   "rationale": "Patient describes chest discomfort..."  │
│ }                                                        │
└─────────────────────────────────────────────────────────┘
```

### 2. RAG Intelligence Flow

```
Regulatory Sources
      │
      ├── FDA MedWatch API
      ├── DailyMed Labels API
      ├── PubMed E-Utilities
      └── DrugBank API
      │
      ▼
┌────────────────────┐
│ Document Ingester  │ ← Scheduled + real-time ingestion
└────────────────────┘
      │
      ├── Chunk documents
      ├── Generate embeddings (medical-optimized)
      └── Store in Vector DB
      │
      ▼
┌────────────────────┐
│   Vector Store     │ ← Qdrant / Pinecone
│   (Embeddings)     │
└────────────────────┘
      │
      │  User Query
      ▼
┌────────────────────┐
│  Hybrid Retrieval  │
│  • Vector Search   │ ← Semantic similarity
│  • BM25 Keyword    │ ← Exact term matching
└────────────────────┘
      │
      ▼
┌────────────────────┐
│  Source Reranker   │ ← Priority: FDA > DailyMed > PubMed
└────────────────────┘
      │
      ▼
┌────────────────────┐
│ Citation Verifier  │ ← Validates source authenticity
└────────────────────┘
      │
      ▼
Intelligence Feed Output
```

### 3. Fair Balance Asset Generation Flow

```
Drug Context + Clinical Translation
            │
            ▼
┌────────────────────┐
│  RAG Drug Lookup   │ ← Fetches latest drug information
└────────────────────┘
            │
            ▼
┌────────────────────┐
│ Black Box Warning  │ ← Mandatory inclusion check
│     Checker        │
└────────────────────┘
            │
            ▼
┌────────────────────┐
│ Benefit Extractor  │ ← Identifies therapeutic benefits
└────────────────────┘
            │
            ▼
┌────────────────────┐
│  Risk Extractor    │ ← Identifies risks & contraindications
└────────────────────┘
            │
            ▼
┌────────────────────┐
│ Fair Balance       │ ← Ensures benefit:risk ratio compliance
│   Validator        │
└────────────────────┘
            │
            ▼
┌────────────────────┐
│ Asset Generator    │ ← Generates structured education card
└────────────────────┘
            │
            ▼
┌────────────────────┐
│ Compliance Stamper │ ← Adds disclaimers + HCP notice
└────────────────────┘
            │
            ▼
┌────────────────────┐
│   PDF/PNG Export   │ ← Final renderable output
└────────────────────┘
```

---

## Technology Stack Justification

### Backend: FastAPI (Python)

**Rationale:**
- **Async-first**: Essential for handling concurrent LLM calls and external API requests
- **Type safety**: Pydantic models ensure data validation at API boundaries
- **Medical ecosystem**: Python has the richest NLP/ML libraries (spaCy, transformers, scispaCy)
- **Compliance**: Easy audit logging with middleware patterns
- **OpenAPI**: Auto-generated API documentation for regulatory review

### AI/ML Layer

| Component | Technology | Justification |
|-----------|------------|---------------|
| LLM Orchestration | LangChain | Standardized chain patterns, memory management |
| Language Detection | fastText / langdetect | 100+ languages, fast inference |
| Medical NER | scispaCy + en_core_sci_lg | Pre-trained on biomedical text |
| Embeddings | BGE-M3 / PubMedBERT | Medical domain optimization |
| Vector Store | Qdrant | Self-hosted option for PHI compliance |
| Safety Classifier | Custom fine-tuned classifier | Detect diagnostic/prescriptive language |

### Database Layer

| Store | Technology | Purpose |
|-------|------------|---------|
| Relational | PostgreSQL 16 | Structured data, ACID compliance |
| Vector | Qdrant | Semantic search over medical documents |
| Cache | Redis | Session state, rate limiting |
| Object | MinIO/S3 | PDF/PNG asset storage |

### Frontend: React + TypeScript

**Rationale:**
- **Existing codebase**: Leveraging current React components
- **Type safety**: TypeScript catches errors at compile time
- **Real-time**: WebSocket integration for streaming responses
- **Export**: html2canvas + jsPDF for client-side PDF generation

---

## Security & Compliance Architecture

### Data Protection (DPDP Act 2023 Compliance)

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA FLOW BOUNDARY                        │
│                                                              │
│  ┌──────────┐     ┌────────────┐     ┌────────────────────┐ │
│  │  User    │────▶│ PII Filter │────▶│  Anonymized        │ │
│  │  Input   │     │            │     │  Processing Zone   │ │
│  └──────────┘     └────────────┘     └────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│                   ┌────────────┐                             │
│                   │ Audit Log  │                             │
│                   │(Encrypted) │                             │
│                   └────────────┘                             │
└─────────────────────────────────────────────────────────────┘

PII Detection & Removal:
• Names (regex + NER)
• Phone numbers
• Email addresses
• Aadhaar numbers
• Medical record numbers
• Dates of birth
```

### Audit Trail Schema

Every operation is logged:
- Timestamp (UTC)
- User ID (anonymized)
- Operation type
- Input hash (not content)
- Output hash
- Confidence scores
- Compliance flags

### Medical Safety Constraints

The system implements a **safety classifier** that blocks:
1. ❌ Diagnostic statements ("You have diabetes")
2. ❌ Prescription recommendations ("Take 500mg of...")
3. ❌ Treatment advice ("You should undergo surgery")
4. ❌ Prognosis statements ("This will get worse")

Allowed outputs:
1. ✅ Clinical terminology mapping
2. ✅ Educational information (with disclaimers)
3. ✅ Regulatory alerts (sourced + verified)

---

## API Contract Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/slang/translate` | POST | Translate patient language to clinical terms |
| `/api/v1/slang/languages` | GET | List supported input languages |
| `/api/v1/rag/intel-feed` | GET | Fetch regulatory intelligence feed |
| `/api/v1/rag/search` | POST | Search drug/regulatory information |
| `/api/v1/rag/verify-source` | GET | Verify a source citation |
| `/api/v1/assets/generate` | POST | Generate patient education asset |
| `/api/v1/assets/{id}` | GET | Retrieve generated asset |
| `/api/v1/export/pdf` | POST | Export asset as PDF |
| `/api/v1/export/png` | POST | Export asset as PNG |
| `/api/v1/audit/logs` | GET | Retrieve audit logs (admin) |
| `/api/v1/health` | GET | System health check |

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTION ENVIRONMENT                   │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Nginx     │  │  FastAPI    │  │   Background        │  │
│  │   Gateway   │──│  Workers    │──│   Workers (Celery)  │  │
│  │   (TLS)     │  │  (Uvicorn)  │  │   • RAG Ingestion   │  │
│  └─────────────┘  └─────────────┘  │   • PDF Generation  │  │
│         │                          └─────────────────────┘  │
│         │                                                    │
│  ┌──────┴──────────────────────────────────────────────┐    │
│  │                   DATA LAYER                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │PostgreSQL│  │  Qdrant  │  │  Redis   │           │    │
│  │  │(Primary) │  │ (Vector) │  │ (Cache)  │           │    │
│  │  └──────────┘  └──────────┘  └──────────┘           │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Non-Functional Requirements

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| Response Time | < 3s for translations | Async processing, caching |
| Throughput | 100 req/sec | Horizontal scaling |
| Availability | 99.9% | Multi-AZ deployment |
| Data Retention | 7 years (audit) | Encrypted archives |
| Encryption | AES-256 at rest | PostgreSQL TDE |
| Transport | TLS 1.3 | Nginx termination |

---

## Success Metrics

1. **Translation Accuracy**: >85% clinician approval rate
2. **Source Verification**: 100% citations verifiable
3. **Fair Balance Compliance**: 100% assets pass automated audit
4. **Zero Hallucinations**: No unsourced medical claims
5. **Audit Completeness**: 100% operations logged

---

*Document Version: 1.0*
*Last Updated: 2026-01-31*
*Classification: Internal - Technical*
