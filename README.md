# 🏛️ Paeon AI: The Clinical-to-Vernacular Bridge

**Digital Medical Representative (DMR) System for Pharma Market Intelligence**

*Developed by: **Shaurya Jain, Swapneel Premchand, Suchethan PH, and Tanvir Singh Sandhu***  
*Built for Plaksha MEDITHON 2026*

---

## 📋 Project Overview

**Paeon AI** is a sophisticated regulated clinical intelligence system named after Paeon, the physician to the Greek gods. It bridges the critical communication gap between patients, healthcare professionals (HCPs), and pharmaceutical data.

> ⚠️ **IMPORTANT**: This is NOT a chatbot. This is a **regulated clinical intelligence system** with strict compliance guardrails designed for healthcare professionals.

### 🎯 Core Mission

Transform colloquial patient descriptions (20+ languages) into structured clinical terminology with standardized medical codes, FDA intelligence, and compliant healthcare assets.

---

## ✨ Key Features

### 1. 🗣️ The Paeon Interpreter (Slang-to-Clinical Engine)

**The Problem:** Patients describe symptoms using regional slang (*"my chest feels like a drum"*, *"my feet are on fire"*), leading to clinical misinterpretation and poor data collection.

**The Solution:** 
- NLP layer mapping vernacular language to standardized medical taxonomies (SNOMED-CT/ICD-10/UMLS)
- 50+ pre-curated mappings for instant clinical interpretation
- Google Gemini AI fallback for unknown symptoms
- Multi-language support (20+ languages auto-detected)
- **PII Protection**: Automatic stripping of personal health information (DPDP Act 2023 compliant)

**Confidence Scoring:**
- Curated mappings: **95%** confidence (instant response)
- AI fallback: **75%** confidence (handles unique symptoms)
- Processing time: 45-200ms

### 2. 📋 The Oracle Feed (RAG-Driven Intelligence)

**Real-Time Medical Intelligence:**
- 🚨 FDA MedWatch alerts and drug recalls
- 💊 Medication label changes and updates
- ⚠️ Safety communications and warnings
- 📰 Clinical research highlights
- 🏥 Healthcare facility alerts

**Features:**
- Hybrid search (vector + keyword for maximum accuracy)
- Source verification with confidence scoring
- Real-time updates from FDA, DailyMed, and PubMed
- Every claim traceable to official sources
- Alert prioritization by severity

### 3. 🎨 Automated Asset Pipeline

- Instant compliant patient education cards
- HCP deep-dive clinical decks
- Automatic "Fair Balance" safety disclosures
- Boxed warning injection
- Professional PDF & shareable formats
- Regulatory audit trail

---

## 🛡️ Safety & Compliance

- **Decision Support Tool**: Explicitly framed as CDS; blocks diagnostic/prescriptive language
- **Hallucination Shield**: Mandatory citations for all clinical claims
- **Zero-Retention Policy**: No PII stored or logged
- **Audit Trail**: Complete compliance logging
- **Fair Balance Compliant**: Automatic safety disclosure injection
- **HIPAA Ready**: No patient data persistence

---

## 🛠️ Technical Stack

| Category | Technology |
|----------|------------|
| **Frontend** | React 18, TypeScript, Tailwind CSS, Shadcn/UI, Zustand |
| **Backend** | FastAPI (Python 3.11+), Pydantic |
| **AI/ML** | Google Gemini 2.5 Flash, LangChain |
| **Data** | SNOMED-CT, ICD-10, UMLS mappings |
| **Compliance** | PII stripping, audit logs, Fair Balance injection |
| **APIs** | FDA MedWatch, DailyMed, PubMed |

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key (FREE - get it in 2 minutes)

### Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Select your existing project or create a new one
4. Copy the generated API key
5. **Keep this key safe** - you'll need it in Step 3

### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv_prod

# Activate virtual environment (Windows)
.\venv_prod\Scripts\activate

# Activate virtual environment (macOS/Linux)
# source venv_prod/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
# Option 1: Create file manually
# Create a file called ".env" in the backend/ folder with these contents:
# GEMINI_API_KEY=your-api-key-here
# GEMINI_MODEL=gemini-2.5-flash

# Option 2: Use command line
echo GEMINI_API_KEY=your-api-key-here > .env
echo GEMINI_MODEL=gemini-2.5-flash >> .env
```

### Step 3: Setup Frontend

```bash
cd ..  # Go back to root directory

# Install dependencies
npm install
```

### Step 4: Run Everything

**Terminal 1 - Start Backend:**
```bash
cd backend
.\venv_prod\Scripts\activate  # Windows
# source venv_prod/bin/activate  # macOS/Linux
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
npm run dev
```

**Open in Browser:**
- Frontend: http://localhost:5173
- API Docs: http://127.0.0.1:8000/docs

---

## 📖 How to Use

### Web Interface

1. Open http://localhost:5173 in your browser
2. Go to **"Slang Translator"** section
3. Enter a patient symptom (e.g., "my feet are burning")
4. Click **Translate**
5. See the clinical term, confidence score, and medical codes

### API Endpoint

```bash
curl -X POST http://127.0.0.1:8000/api/v1/slang/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "my feet are burning"}'
```

**Response:**
```json
{
  "clinical_interpretation": "Burning Feet Sensation",
  "confidence": 0.95,
  "standard_codes": [
    {
      "system": "SNOMED-CT",
      "code": "39072002"
    },
    {
      "system": "ICD-10",
      "code": "R20.8"
    }
  ],
  "rationale": "Matched curated mapping for 'burning feet'",
  "processing_time_ms": 45
}
```

---

## 📋 Intelligence Feed - FDA Tracking & Medical Intelligence

### What It Does

The Intelligence Feed provides real-time medical intelligence to healthcare professionals, including:

- **🚨 FDA MedWatch Alerts** - Drug recalls, safety warnings, adverse event reports
- **💊 Drug Recalls** - Immediate notification of recalled medications
- **⚠️ Safety Alerts** - Healthcare facility safety notices
- **📰 Medical Updates** - Latest clinical research and guidelines
- **🏥 Healthcare News** - Important news for medical professionals

### How It Works

The system automatically fetches and curates data from:

1. **FDA MedWatch Database**
   - Real-time adverse event reports
   - Drug recalls and withdrawals
   - Medical device safety alerts
   - Dietary supplement warnings

2. **DailyMed**
   - FDA drug label database
   - Medication information updates
   - Safety information changes

3. **Curated Medical Sources**
   - Healthcare professional warnings
   - Clinical practice updates
   - Regulatory announcements

### Using the Intelligence Feed

1. Open the web interface at http://localhost:5173
2. Click on **"Intelligence Feed"** tab
3. Browse real-time medical updates
4. Click **"Source"** to see where information came from
5. Filter by alert type (if available)

### Intelligence Feed API

Get medical intelligence programmatically:

```bash
curl -X GET http://127.0.0.1:8000/api/v1/intelligence/feed \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "feed": [
    {
      "title": "FDA Alert: Drug Name Recall",
      "description": "The FDA has recalled...",
      "alert_type": "drug_recall",
      "severity": "high",
      "source": "FDA MedWatch",
      "published_date": "2026-02-01T10:30:00Z",
      "link": "https://fda.gov/..."
    },
    {
      "title": "Safety Alert: Device Issue",
      "description": "Healthcare facilities should...",
      "alert_type": "safety_alert",
      "severity": "medium",
      "source": "FDA Safety",
      "published_date": "2026-02-01T09:15:00Z",
      "link": "https://fda.gov/..."
    }
  ]
}
```

### Alert Types

| Type | Description | Source | Update Frequency |
|------|-------------|--------|------------------|
| **drug_recall** | Medication recalls | FDA MedWatch | Real-time |
| **device_alert** | Medical device warnings | FDA MedWatch | Real-time |
| **adverse_event** | Patient adverse events | FDA MedWatch | Daily |
| **safety_alert** | Healthcare safety notices | FDA | Daily |
| **drug_label_update** | Medication label changes | DailyMed | Daily |
| **clinical_update** | Medical guidelines update | Curated | Weekly |

### Example: Get Drug Recalls Only

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/intelligence/feed?filter=drug_recall"
```

### Real-World Examples

**Example 1: FDA Recalls Blood Pressure Medication**
```
Alert Type: drug_recall
Severity: HIGH
Message: "FDA recalls [Drug Name] due to contamination risk"
Action: Healthcare providers should notify patients
```

**Example 2: Device Safety Update**
```
Alert Type: device_alert
Severity: MEDIUM
Message: "Cardiac monitor may have display issue"
Action: Software update available from manufacturer
```

**Example 3: Adverse Event Report**
```
Alert Type: adverse_event
Severity: MEDIUM
Message: "Reports of [Side Effect] with [Drug Name]"
Action: Evaluate risk-benefit for new patients
```

---

## ⚙️ Configuration

### Edit Your API Key

If you need to change your API key later:

**Windows:**
```powershell
# Edit the .env file in backend folder
notepad backend\.env
```

**macOS/Linux:**
```bash
nano backend/.env
```

Then change the line:
```
GEMINI_API_KEY=your-new-api-key-here
```

Restart the backend server after changing the key.

### .env File Reference

```env
# REQUIRED: Your Google Gemini API Key (get from https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your-api-key-here

# OPTIONAL: Model to use (default: gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash

# OPTIONAL: Environment type
ENVIRONMENT=development

# OPTIONAL: Application name
APP_NAME=Paeon AI
```

---

## 🧠 How It Works

### Two-Tier Smart Mapping

#### Tier 1: Curated Mappings (Fast & Accurate)
- **50+ common symptoms** pre-mapped to medical terms
- **95%+ confidence**
- **Instant response** (no API delay)
- Examples: "burning feet", "chest pain", "dizzy", "cold"

#### Tier 2: AI Fallback (Flexible)
- Uses **Google Gemini AI** for unknown symptoms
- **75% confidence**
- Handles unique/specific symptoms
- Examples: "ears ringing", "jaw pain", "can't see clearly"

### Supported Curated Symptoms

**Cardiac Symptoms:**
- Heart feels funny → Palpitations
- Chest is tight → Chest Tightness
- Heart racing → Tachycardia

**Respiratory:**
- Cold → Upper Respiratory Infection
- Can't breathe → Dyspnea
- Wheezing → Wheezing

**Gastrointestinal:**
- Feeling bloated → Bloating
- Throwing up → Vomiting
- Belly hurts → Abdominal Pain

**Neurological:**
- Head is pounding → Headache
- Dizzy → Dizziness
- Burning feet → Burning Feet Sensation

**Musculoskeletal:**
- Back pain → Back Pain
- Muscles ache → Myalgia
- Neck pain → Cervical Pain

**And 20+ more symptoms...**

---

## 🌍 Supported Languages

Automatically detects and translates from:
- **English, Hindi, Spanish, French, German, Portuguese**
- **Chinese (Simplified), Japanese, Korean, Arabic, Russian**
- **Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu**

---

## 🔍 Example Requests

### Example 1: Known Symptom (Curated)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/slang/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "cold"}'
```
**Result:** Upper Respiratory Infection (95% confidence)

### Example 2: Unknown Symptom (LLM)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/slang/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "my ears are ringing"}'
```
**Result:** Tinnitus (75% confidence)

### Example 3: Multi-language Input
```bash
curl -X POST http://127.0.0.1:8000/api/v1/slang/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "mere seene mein dard"}'
```
**Result:** Chest Pain (translated from Hindi)

---

## 🐛 Troubleshooting

### "API Key Error" or "Invalid API Key"

**Solution:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key (or verify your existing one is active)
3. Update your `backend/.env` file with the correct key
4. Restart the backend server

### "Backend not responding"

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
.\venv_prod\Scripts\activate  # Windows

# Start the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### "Port 8000 already in use"

**Solution (Windows):**
```powershell
# Find and kill process using port 8000
Get-Process | Where-Object { $_.Handles -like "*8000*" } | Stop-Process -Force

# Or use a different port
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### "npm command not found"

**Solution:**
- Install Node.js from https://nodejs.org (includes npm)
- Restart your terminal after installation

---

## 📁 Project Structure

```
Paeon-AI/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # REST endpoints
│   │   ├── services/          # Business logic
│   │   ├── core/              # Configuration & settings
│   │   └── __main__.py
│   ├── requirements.txt        # Python packages
│   ├── .env                   # Your API key (not in git)
│   └── venv_prod/             # Virtual environment
├── src/                        # React frontend
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   ├── styles/                # CSS
│   └── main.tsx
├── package.json               # Node dependencies
├── vite.config.ts             # Vite config
└── README.md                  # This file
```

---

## 🔐 Security Notes

- **API keys are sensitive**: Never commit your `.env` file to Git
- The `.env` file is already in `.gitignore`
- Use different API keys for development and production
- Monitor your API usage at [Google Cloud Console](https://console.cloud.google.com)

---

## 📚 Full API Documentation

Once the backend is running, visit:
```
http://127.0.0.1:8000/docs
```

This shows interactive API documentation with all available endpoints.

---

## ⚠️ Important Disclaimer

**For Healthcare Professional Use Only**

This system is **NOT a diagnostic tool**. It only:
- Translates patient language to medical terminology
- Provides standardized medical codes
- Shows confidence scores for accuracy

It does **NOT**:
- Diagnose conditions
- Recommend treatments
- Suggest medications
- Provide medical advice

**Always consult with qualified healthcare professionals for diagnosis and treatment.**

---

## 🎓 How to Get Started (Step-by-Step)

### Complete Beginner Guide

1. **Install Python** (if not already installed)
   - Download from https://www.python.org
   - Make sure to check "Add Python to PATH"

2. **Install Node.js** (if not already installed)
   - Download from https://nodejs.org
   - Includes npm

3. **Get Gemini API Key** (2 minutes)
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy and save it

4. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv_prod
   .\venv_prod\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Create .env file**
   - Create a file named `.env` in `backend/` folder
   - Add: `GEMINI_API_KEY=your-api-key-here`
   - Add: `GEMINI_MODEL=gemini-2.5-flash`

6. **Setup Frontend**
   ```bash
   cd ..
   npm install
   ```

7. **Run it!**
   - Terminal 1: `cd backend` → `.\venv_prod\Scripts\activate` → `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
   - Terminal 2: `npm run dev`
   - Open http://localhost:5173

---

## 💡 Tips & Tricks

- **Test the API first**: Use the interactive docs at http://127.0.0.1:8000/docs
- **Check logs**: Look at terminal output to see what's happening
- **Use common symptoms**: Try "cold", "fever", "headache" to test quickly
- **Monitor API usage**: Check https://aistudio.google.com to see your usage

---

## 📞 Need Help?

1. **Check the Troubleshooting section** above
2. **Read API documentation** at http://127.0.0.1:8000/docs
3. **Look at example requests** in this README
4. **Check backend logs** in the terminal where it's running

---

**Built with ❤️ for Medithon 2026**  
*By: Shaurya Jain, Swapneel Premchand, Suchethan PH, and Tanvir Singh Sandhu*
