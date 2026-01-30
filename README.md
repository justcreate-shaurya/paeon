
  # Design LinguPharma AI Dashboard
  DEVELOPED BY Shaurya Jain, Swapneel Premchand, Suchethan PH and Tanvir Singh Sandhu.

  # Paeon AI: The Clinical-to-Vernacular Bridge

*Pharma Market Intelligence & Digital Medical Representation for the Plaksha MEDITHON*


 🏛️ Project Overview

*Paeon AI* is a sophisticated, "Fair Balance" compliant digital agent named after the physician to the Greek gods. It bridges the critical communication gap between patients, healthcare professionals (HCPs), and pharmaceutical data.

By utilizing a unique *Slang-to-Clinical Engine*, Paeon AI translates colloquial patient descriptions into structured medical history, while a robust **RAG (Retrieval-Augmented Generation) pipeline** ensures that HCPs receive real-time, grounded information on drug recalls, side effects, and reimbursement protocols.

## ✨ Key Features

### 1. The Paeon Interpreter (Slang-to-Symptom)

* **The Problem:** Patients often describe symptoms using regional slang or vague metaphors (e.g., *"my chest feels like a drum"*), which can lead to clinical misinterpretation.
* **The Solution:** An NLP layer that maps vernacular language to standardized medical taxonomies (SNOMED-CT/UMLS), allowing the Medical Rep to take accurate, empathetic histories.

### 2. The Oracle Feed (RAG-Driven Intelligence)

 **Real-Time Accuracy:** Unlike standard LLMs, Paeon uses Hybrid Search (Vector + Keyword) to query live databases like **openFDA**, **DailyMed**, and **PubMed**.
 **Safety First:** Tracks drug recalls and newly identified side effects instantly, providing a "Source View" for every claim to eliminate hallucinations.

### 3. Automated Asset Pipeline

 **Instant Education:** Generates mobile-responsive **Patient Action Cards** and **HCP Deep-Dive Decks**.
 **Fair Balance Engine:** Automatically injects mandatory safety disclosures and "Boxed Warnings" into every promotional asset, ensuring regulatory compliance by design.

---

## 🛠️ Technical Stack

| Layer | Technology |
| --- | --- |
| **Frontend** | Next.js 15, Tailwind CSS, Shadcn/UI |
| **Design System** | Minimalist White & Dark Olive Green (#3B4D2B) |
| **LLM Orchestration** | LangChain / LlamaIndex |
| **Vector Database** | Pinecone / Weaviate (Hybrid Search) |
| **Knowledge Base** | OpenFDA API, DailyMed, PubMed Central |
| **Compliance** | PII Anonymization Layer (HIPAA/DPDP compliant) |

---

## 🏗️ Architecture

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

---

## 🚀 Getting Started

### Prerequisites

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


## 👥 The Team

Built with 💚 for **Plaksha MEDITHON 2026**
