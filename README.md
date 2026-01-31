
<<<<<<< HEAD
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
=======
  # Design LinguPharma AI Dashboard
  DEVELOPED BY Shaurya Jain, Swapneel Premchand, Suchethan PH and Tanvir Singh Sandhu.

  # Paeon AI: The Clinical-to-Vernacular Bridge

*Pharma Market Intelligence & Digital Medical Representation for the Plaksha MEDITHON*


 🏛️ Project Overview

*Paeon AI* is a sophisticated, "Fair Balance" compliant digital agent named after the physician to the Greek gods. It bridges the critical communication gap between patients, healthcare professionals (HCPs), and pharmaceutical data.

By utilizing a unique *Slang-to-Clinical Engine*, Paeon AI translates colloquial patient descriptions into structured medical history, while a robust **RAG (Retrieval-Augmented Generation) pipeline** ensures that HCPs receive real-time, grounded information on drug recalls, side effects, and reimbursement protocols.
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

## ✨ Key Features

### 1. The Paeon Interpreter (Slang-to-Symptom)

<<<<<<< HEAD
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
=======
* **The Problem:** Patients often describe symptoms using regional slang or vague metaphors (e.g., *"my chest feels like a drum"*), which can lead to clinical misinterpretation.
* **The Solution:** An NLP layer that maps vernacular language to standardized medical taxonomies (SNOMED-CT/UMLS), allowing the Medical Rep to take accurate, empathetic histories.

### 2. The Oracle Feed (RAG-Driven Intelligence)

 **Real-Time Accuracy:** Unlike standard LLMs, Paeon uses Hybrid Search (Vector + Keyword) to query live databases like **openFDA**, **DailyMed**, and **PubMed**.
 **Safety First:** Tracks drug recalls and newly identified side effects instantly, providing a "Source View" for every claim to eliminate hallucinations.

### 3. Automated Asset Pipeline

 **Instant Education:** Generates mobile-responsive **Patient Action Cards** and **HCP Deep-Dive Decks**.
 **Fair Balance Engine:** Automatically injects mandatory safety disclosures and "Boxed Warnings" into every promotional asset, ensuring regulatory compliance by design.
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

---

## 🛠️ Technical Stack

<<<<<<< HEAD
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
=======
| Layer | Technology |
| --- | --- |
| **Frontend** | Next.js 15, Tailwind CSS, Shadcn/UI |
| **Design System** | Minimalist White & Dark Olive Green (#3B4D2B) |
| **LLM Orchestration** | LangChain / LlamaIndex |
| **Vector Database** | Pinecone / Weaviate (Hybrid Search) |
| **Knowledge Base** | OpenFDA API, DailyMed, PubMed Central |
| **Compliance** | PII Anonymization Layer (HIPAA/DPDP compliant) |
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

---

## 🏗️ Architecture

<<<<<<< HEAD
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
=======
1. **Ingestion:** Scrapes official Pharma labels and clinical trial updates.
2. **Processing:** Normalizes patient input via the *Interpreter* module.
3. **Retrieval:** RAG pipeline fetches the most authoritative "Ground Truth."
4. **Verification:** A "Fair Balance" check ensures risk-to-benefit transparency.
5. **Output:** Generates UI-driven dashboards and downloadable PDF/Image assets.

---

## 🛡️ Safety & Compliance (The Guardrails)

* **Decision Support, Not Diagnosis:** Framed strictly as a Clinical Decision Support (CDS) tool.
* **Hallucination Shield:** Mandatory citations for every clinical fact retrieved.
* **Data Privacy:** Zero-retention policy for Personal Identifiable Information (PII) during the translation phase.
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

---

## 🚀 Getting Started

### Prerequisites

<<<<<<< HEAD
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
=======
* Node.js 18+
* Python 3.9+ (for the RAG backend)
* OpenAI / Anthropic API Key (or local Llama 3 instance)

### Installation

1. **Clone the repo:**
```bash
git clone https://github.com/your-username/paeon-ai.git

```


2. **Install dependencies:**
```bash
npm install
pip install -r requirements.txt

```


3. **Run the development server:**
```bash
npm run dev

```

>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

## 👥 The Team

Built with 💚 for **Plaksha MEDITHON 2026**
<<<<<<< HEAD

- Shaurya Jain
- Swapneel Premchand  
- Suchethan PH
- Tanvir Singh Sandhu

---

## 📄 License

This project is developed for educational and demonstration purposes as part of Plaksha MEDITHON 2026.
=======
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
