# Paeon AI: The Clinical-to-Vernacular Bridge

**Digital Medical Representative (DMR) System for Pharma Market Intelligence**

**DEVELOPED BY:** Shaurya Jain, Swapneel Premchand, Suchethan PH, and Tanvir Singh Sandhu  
*Built for Plaksha MEDITHON 2026*

---

## 🏛️ Project Overview

**Paeon AI** is a sophisticated, "Fair Balance" compliant digital agent named after the physician to the Greek gods. It bridges the critical communication gap between patients, healthcare professionals (HCPs), and pharmaceutical data.

> ⚠️ **IMPORTANT**: This is NOT a chatbot. This is a **regulated clinical intelligence system** with strict compliance guardrails.

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **The Paeon Interpreter** | Translates colloquial slang (20+ languages) into structured SNOMED-CT/UMLS medical terminology. |
| **The Oracle Feed** | RAG-driven intelligence providing real-time drug recalls and safety alerts from FDA, DailyMed, and PubMed. |
| **Asset Pipeline** | Generates compliant patient education cards and HCP decks with automatic "Fair Balance" safety disclosures. |

---

## ✨ Key Features

### 1. The Paeon Interpreter (Slang-to-Symptom)
* **The Problem:** Patients describe symptoms using regional slang (e.g., *"my chest feels like a drum"*), leading to clinical misinterpretation.
* **The Solution:** An NLP layer that maps vernacular language to standardized medical taxonomies, ensuring accurate and empathetic history-taking.
* **Compliance:** Automatic PII stripping (DPDP Act 2023 compliant) before clinical use.

### 2. The Oracle Feed (RAG-Driven Intelligence)
* **Real-Time Accuracy:** Uses Hybrid Search (Vector + Keyword) to query live medical databases.
* **Hallucination Shield:** Mandatory citations and "Source View" for every claim retrieved from official sources.
* **Safety First:** Instantly tracks drug recalls and newly identified side effects to keep HCPs updated.

### 3. Automated Asset Pipeline
* **Fair Balance Engine:** Automatically injects mandatory safety disclosures and "Boxed Warnings" into every promotional asset.
* **Instant Education:** Generates mobile-responsive **Patient Action Cards** and **HCP Deep-Dive Decks** in PDF/PNG formats.

---

## 🛠️ Technical Stack

### Frontend & Design
* **Framework:** Next.js 15 / React 18 + TypeScript
* **Styling:** Tailwind CSS + Shadcn/UI
* **Design System:** Minimalist White & Dark Olive (#3B4D2B)
* **State Management:** Zustand

### Backend & AI
* **Framework:** FastAPI (Python 3.11+)
* **Orchestration:** LangChain / LlamaIndex
* **Vector Store:** Qdrant / Pinecone (Hybrid Search)
* **LLM:** OpenAI GPT-4
* **Knowledge Base:** OpenFDA API, DailyMed, PubMed Central

---

## 🛡️ Safety & Compliance

1.  **Decision Support, Not Diagnosis:** Framed strictly as a Clinical Decision Support (CDS) tool; requires HCP approval for clinical use.
2.  **PII Protection:** Zero-retention policy for Personal Identifiable Information during the translation phase.
3.  **Source Verification:** Every output includes a confidence score and direct links to authority sources.

---

## 🚀 Getting Started

### Prerequisites
* Node.js 18+
* Python 3.11+
* OpenAI API Key

### Installation
1.  **Clone and Install:**
    ```bash
    git clone [https://github.com/justcreate-shaurya/paeon.git](https://github.com/justcreate-shaurya/paeon.git)
    npm install
    pip install -r requirements.txt
    ```

2.  **Run Development Servers:**
    ```bash
    # Frontend
    npm run dev

    # Backend
    cd backend
    uvicorn app.main:app --reload
    ```

---

## 👥 The Team
Built with 💚 by **Shaurya Jain, Swapneel Premchand, Suchethan PH, and Tanvir Singh Sandhu.**
