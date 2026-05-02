# 🤖 PDF Extraction Agent

![CI](https://github.com/Nourimanekerroumi996/pdf-extraction-agent/actions/workflows/ci.yml/badge.svg)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://pdf-extraction-agent-17b7.onrender.com)



> An agentic AI system that automatically extracts structured data from any PDF — text, tables, dates, amounts, and names. Upload a PDF, get clean JSON back in seconds.

---
## 🌐 Live Demo

👉 **[Try it here](https://pdf-extraction-agent-17b7.onrender.com)**

> Note: Free instance may take 30-50 seconds to wake up on first request.

---

## What does it do?

You send a PDF. The agent reads it, finds all the important information, and returns everything structured in JSON — automatically, in a few seconds.

It handles:
- 📄 **Regular PDFs** — extracts text directly
- 📊 **Tables** — detects and structures them properly
- 🖼️ **Scanned PDFs** — uses OCR to read images
- 🧠 **Entities** — finds names, dates, amounts and titles using AI

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Nourimanekerroumi996/pdf-extraction-agent
cd pdf-extraction-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Open .env and add your GROQ_API_KEY

# Start the API
uvicorn app.api.main:app --reload
```

Then open **http://localhost:8000/docs** in your browser and upload any PDF.

---

## 🏗️ How it works

```
PDF uploaded
      ↓
FastAPI receives the file
      ↓
LangGraph Agent starts
      │
      ├── Step 1 → pdfplumber    extract raw text
      ├── Step 2 → camelot       extract tables
      ├── Step 3 → pytesseract   OCR for scanned pages
      ├── Step 4 → Groq Llama3   extract names, dates, amounts
      └── Step 5 → Pydantic      validate and structure output
      │
      ↓
Clean JSON returned
```

## 📤 Example Output

Send this invoice:
INVOICE #2024-001
Date: March 12, 2024
Client: Jean Dupont — ABC Consulting
Development: $1500
Meeting: $200
Total: $1700

Get this back:
```json
{
  "filename": "invoice.pdf",
  "pages": 1,
  "titles": ["INVOICE #2024-001"],
  "dates": ["March 12, 2024"],
  "amounts": ["$1500", "$200", "$1700"],
  "names": ["Jean Dupont", "ABC Consulting"],
  "tables": [
    {
      "headers": ["Product", "Price"],
      "rows": [["Development", "$1500"], ["Meeting", "$200"]],
      "page": 1
    }
  ]
}
```

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Agent Orchestration | LangGraph | Controls the pipeline flow |
| LLM | Groq Llama3 | Fast and free entity extraction |
| Text Extraction | pdfplumber | Reliable text from digital PDFs |
| Table Extraction | camelot | Best-in-class PDF table parser |
| OCR | pytesseract | Reads scanned/image PDFs |
| Schema Validation | Pydantic v2 | Guarantees clean output format |
| API | FastAPI | REST interface with auto-docs |
| Containerization | Docker | Runs anywhere, no setup needed |
| CI/CD | GitHub Actions | Auto-tests on every push |

---

## 🐳 Run with Docker

```bash
docker-compose up --build
```

The API will be available at **http://localhost:8000/docs**

---
## 📁 Project Structure

```
pdf-extraction-agent/
│
├── app/
│   ├── agent/          → LangGraph pipeline
│   ├── extractors/     → text, tables, OCR, entities
│   ├── schemas/        → Pydantic output schema
│   ├── api/            → FastAPI endpoints
│   └── storage/        → AWS S3
│
├── tests/
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/  → CI/CD
```

---

## 👩‍💻 Author

**Nour Imane Kerroumi** — Data Scientist & ML Engineer

- 💼 [LinkedIn](https://linkedin.com/in/nour-imane-kerroumi)
- 🐙 [GitHub](https://github.com/Nourimanekerroumi996)