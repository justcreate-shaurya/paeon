
# Paeon AI: The Clinical-to-Vernacular Bridge

*Digital Medical Representative (DMR) System for Pharma Market Intelligence*

**DEVELOPED BY** Shaurya Jain, Swapneel Premchand, Suchethan PH and Tanvir Singh Sandhu  
*Built for Plaksha MEDITHON 2026*

---

## 🏛️ Project Overview

**Paeon AI** is a sophisticated, "Fair Balance" compliant digital agent named after the physician to the Greek gods. It bridges the critical communication gap between patients, healthcare professionals (HCPs), and pharmaceutical data.

> ⚠️ **IMPORTANT**: This is NOT a chatbot. This is a **regulated clinical intelligence system** with strict compliance guardrails.

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Slang-to-Clinical Engine** | Translates colloquial patient descriptions (20+ languages) into structured medical terminology |
| **RAG Intelligence Feed** | Real-time drug recalls, safety alerts, and label updates from FDA/DailyMed/PubMed |
| **Fair Balance Asset Generator** | Compliant patient education cards with automatic safety disclosures |

---

## ✨ Key Features

### 1. The Paeon Interpreter (Slang-to-Symptom)

- **Multi-Language Support**: Hindi, Tamil, Telugu, Spanish, German + 15 more
- **Clinical Mapping**: Maps to SNOMED-CT, ICD-10, UMLS codes
- **PII Protection**: Automatic stripping of personal health information (DPDP Act 2023 compliant)
- **HCP Workflow**: Approve/Edit translations before clinical use

### 2. The Oracle Feed (RAG-Driven Intelligence)

- **Real-Time Updates**: FDA drug recalls, safety communications, label changes
- **Hybrid Search**: Vector + keyword search for maximum accuracy
- **Source Verification**: Every claim traceable to official FDA/PubMed sources
- **Semantic Relevance**: Relevance scoring for search results

### 3. Automated Asset Pipeline

- **Patient Education Cards**: Mobile-responsive, downloadable PDF/PNG
- **Fair Balance Engine**: Auto-injects required safety disclosures
- **Compliance Scoring**: Real-time compliance verification
- **Export Formats**: Professional PDF and shareable PNG formats

---

## 🛠️ Technical Stack

### Frontend
| Layer | Technology |
|-------|------------|
| **Framework** | React 18 + TypeScript |
| **Build Tool** | Vite 5 |
| **Styling** | Tailwind CSS + Shadcn/UI |
| **State** | Zustand |
| **HTTP** | Axios |
| **Design System** | Minimalist White & Dark Olive (#3B4D2B) |

### Backend
| Layer | Technology |
|-------|------------|
| **Framework** | FastAPI (Python 3.11+) |
| **Database** | PostgreSQL 16 + SQLAlchemy |
| **Vector Store** | Qdrant (self-hosted for PHI compliance) |
| **Cache** | Redis |
| **AI/ML** | OpenAI GPT-4, LangChain |
| **NLP** | langdetect, scispaCy concepts |

### Compliance
| Requirement | Implementation |
|-------------|----------------|
| **DPDP Act 2023** | PII stripping, audit logs, data minimization |
| **Fair Balance** | Automatic safety disclosure injection |
| **CDS Guidelines** | Non-diagnostic framing, HCP-only workflows |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PAEON AI SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   COLUMN 1   │    │   COLUMN 2   │    │   COLUMN 3   │      │
│  │  Slang-to-   │    │ Intelligence │    │  Live Asset  │      │
│  │   Clinical   │    │     Feed     │    │   Preview    │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Backend                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ Translation │  │     RAG     │  │    Asset    │      │   │
│  │  │   Engine    │  │   Engine    │  │   Engine    │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│         ┌────────────────────┼────────────────────┐            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │ PostgreSQL  │      │   Qdrant    │      │   OpenAI    │    │
│  │  (Audit)    │      │  (Vectors)  │      │   GPT-4     │    │
│  └─────────────┘      └─────────────┘      └─────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 16+
- **Redis** (optional, for caching)
- **OpenAI API Key** (or compatible LLM endpoint)

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/paeon-ai.git
cd paeon-ai/paeon
```

2. **Install Frontend Dependencies:**
```bash
npm install
```

3. **Install Backend Dependencies:**
```bash
cd backend
pip install -e .
# or with poetry:
poetry install
```

4. **Configure Environment:**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys and database credentials
```

5. **Start Development Servers:**

```bash
# Terminal 1 - Frontend
npm run dev

# Terminal 2 - Backend
cd backend
uvicorn app.main:app --reload --port 8000
```

6. **Access the Application:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
paeon/
├── src/                      # Frontend source
│   ├── components/           # React components
│   │   ├── SlangTranslator.tsx
│   │   ├── IntelligenceFeed.tsx
│   │   ├── LiveAssetPreview.tsx
│   │   └── ui/               # Shadcn components
│   ├── lib/
│   │   ├── api.ts            # API client
│   │   └── store.ts          # Zustand stores
│   └── App.tsx
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── services/         # Business logic
│   │   │   ├── slang/        # Translation engine
│   │   │   ├── rag/          # Intelligence engine
│   │   │   ├── assets/       # Asset generation
│   │   │   └── compliance/   # PII & safety
│   │   ├── db/               # Database models
│   │   └── schemas/          # Pydantic schemas
│   └── prompts/              # LLM prompt templates
├── ARCHITECTURE.md           # Detailed system design
└── package.json
```

---

## 🛡️ Safety & Compliance

### The Guardrails

1. **Decision Support, Not Diagnosis**
   - System explicitly framed as CDS tool
   - Blocks diagnostic/prescriptive language
   - Requires HCP approval for clinical use

2. **Hallucination Shield**
   - Mandatory citations for all claims
   - Source verification badges
   - Confidence scoring on all outputs

3. **Data Privacy (DPDP Act 2023)**
   - Zero PII retention in translation pipeline
   - Immutable audit logs
   - Anonymization of all patient data

---

## 📊 Demo Mode

The application includes comprehensive demo data for testing without a backend:

- **Pre-loaded translations** with various languages
- **Sample intelligence feed** with FDA recalls and updates
- **Demo patient education cards** with compliance scoring

Toggle "Regulatory Guardrails" in the header to see Fair Balance warnings.

---

## 👥 The Team

Built with 💚 for **Plaksha MEDITHON 2026**

- Shaurya Jain
- Swapneel Premchand  
- Suchethan PH
- Tanvir Singh Sandhu

---

## 📄 License

This project is developed for educational and demonstration purposes as part of Plaksha MEDITHON 2026.
