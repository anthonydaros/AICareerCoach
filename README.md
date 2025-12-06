# AI Career Coach - Intelligent Career Assistant

![Project Status](https://img.shields.io/badge/status-MVP-blue)
![License](https://img.shields.io/badge/license-Portfolio-green)

**AI Career Coach** is a specialized tool for automated career optimization. It ingests Job Descriptions and Resumes, analyzes alignment using local LLMs (Llama 3 via Ollama), and provides actionable strategies to increase interview chances.

> **Disclaimer**: This is a technical portfolio project by **[Anthony Max](http://anthonymax.com/)**. It demonstrates architecture and AI integration skills. **It offers no guaranteed job placement.**

## 🏗 System Architecture

The project is built as a distributed system with a strict separation of concerns (Clean Architecture).

### Backend (`/backend`)
A high-performance **FastAPI** service responsible for document processing and LLM orchestration.
- **Runtime**: Python 3.10+
- **API**: FastAPI (Async/Await)
- **AI Integration**: Custom Gateway using `OpenAI` SDK to communicate with **Ollama** (Llama 3).
- **Document Parsing**:
  - `PyPDF2` / `pdfminer` for PDF extraction.
  - `python-docx` for Word documents.
- **Architecture**: Domain-Driven Design (DDD) layers (`domain`, `application`, `infrastructure`, `presentation`).

### Frontend (`/frontend`)
A modern, reactive UI built for speed and accessibility, featuring a Gamified "Cyberpunk" HUD.
- **Framework**: Next.js 16 (App Router)
- **State/UI**: React 19, Tailwind CSS, Shadcn/UI.
- **Visuals**: `Framer Motion` for complex animations (Stack Cards, HUD interactions).
- **Client Features**:
  - **Gamified HUD**: "Mission Intel" & "Loadout" interfaces.
  - **aceternity-ui** inspired effects.
  - Real-time streaming response visualization.

## 🚀 Quick Start

### Prerequisites
1.  **Docker & Docker Compose** (Recommended)
2.  **Ollama** installed on host machine (`ollama serve`).
3.  Pull model: `ollama run llama3` (or configured model).

### Option 1: Docker (Recommended)
The project is configured with a unified environment.

1.  **Configure Environment**
    ```bash
    cp .env.example .env
    # Edit .env if needed
    ```

2.  **Run Application**
    ```bash
    docker-compose up --build
    ```
    The app will be available at **http://localhost:3000**.

### Option 2: Manual Setup

#### 1. Backend Service
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Server
export $(cat ../.env | xargs) && uvicorn src.presentation.api.main:app --reload --port 8000
```

#### 2. Frontend Application
```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```

The app will be available at **http://localhost:3000**.

## 🔌 API Endpoints

- `POST /api/upload`: Upload Resume (PDF/DOCX). Returns parsed text and metadata.
- `POST /api/analyze`: Trigger LLM analysis on Job Description vs Resume.
- `GET /health`: Service health check.

## 🛠 Project Structure

```bash
.
├── backend
│   ├── src
│   │   ├── application    # Use cases (AnalyzeResume, MatchJob)
│   │   ├── domain         # Entities (Resume, JobDescription), Interfaces
│   │   ├── infrastructure # Parsers, LLM Gateway (Ollama)
│   │   └── presentation   # API Routes & Main entry point
│   └── requirements.txt
└── frontend
    └── src/app            # Next.js Pages (Dashboard, Analysis)
    └── src/components     # Reusable UI (Game HUD, Stack Input, Resume Uploader)
```

## 🔒 Security & Privacy

- **Local Processing**: By default, this system connects to a local Ollama instance. No data leaves your machine if configured locally.
- **No Persistence**: The MVP uses in-memory or temporary storage for the session.
- **Stealth Mode**: Frontend configured with `noindex` SEO headers.

## 👨‍💻 Author

**Anthony Max**
*AI Product Builder | Full Stack Engineer*

- [Website](http://anthonymax.com/)
- [GitHub](https://github.com/anthonydaros)
