# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Career Coach MVP - An AI-powered career assistant that analyzes resume ATS compatibility, matches against multiple job postings, and generates interview preparation materials. Uses a self-hosted Ollama server with OpenAI-compatible API.

## Development Commands

### Frontend (Next.js 16)
```bash
cd frontend
npm run dev      # Start dev server on localhost:3000
npm run build    # Production build
npm run lint     # Run ESLint
```

### Backend (FastAPI)
```bash
cd backend
uvicorn src.presentation.api.main:app --reload --port 8000
```

### Docker (Full Stack)
```bash
docker-compose up           # Frontend: 3001, Backend: 8001
docker-compose up --build   # Rebuild images
```

## Architecture

### Backend (Clean Architecture / DDD)
```
backend/src/
├── domain/           # Business logic (entities, interfaces, services)
│   ├── entities/     # Resume, JobPosting, ATSResult, JobMatch
│   ├── interfaces/   # ILLMGateway, IVectorStore, IDocumentParser
│   └── services/     # ATSScorer, JobMatcher, InterviewGenerator
├── application/      # Use cases and DTOs
│   ├── use_cases/    # ParseResume, CalculateATS, MatchJobs, etc.
│   └── dtos/         # Input/output data transfer objects
├── infrastructure/   # External implementations
│   ├── llm/          # OpenAI SDK client pointing to Ollama
│   ├── vectorstore/  # FAISS for skill embeddings
│   ├── parsers/      # PDF/DOCX/TXT document parsers
│   └── langchain/    # LangChain LCEL chains
└── presentation/     # FastAPI routes and schemas
    └── api/main.py   # FastAPI application entry point
```

### Frontend (Next.js App Router)
```
frontend/
├── app/              # Next.js 16 App Router
│   ├── page.tsx      # Main dashboard (client component)
│   ├── layout.tsx    # Root layout with fonts
│   └── globals.css   # Tailwind + CSS variables
└── components/
    ├── ui/           # shadcn/ui base components
    ├── layout/       # Header, Footer, Background
    ├── upload/       # ResumeUploader (drag-drop)
    ├── input/        # JobPostInput (multi-job text input)
    └── preview/      # LivePreview (analysis results)
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16, React 19, TailwindCSS, Framer Motion, shadcn/ui |
| Backend | Python 3.10+, FastAPI, Pydantic v2 |
| AI | LangChain, OpenAI SDK (Ollama backend), FAISS |
| Document Parsing | PyMuPDF, python-docx |

## Configuration

Environment variables in `.env`:
- `OPENAI_BASE_URL` - Ollama server URL (e.g., `https://ollama.anthonymax.com/v1`)
- `OPENAI_API_KEY` - API key for Ollama (can be `ollama`)
- `OPENAI_MODEL` - LLM model (e.g., `granite4:7b`)
- `OPENAI_EMBEDDING_MODEL` - Embedding model (e.g., `nomic-embed-text`)
- `ALLOWED_ORIGINS` - CORS origins for frontend

## Key API Endpoints (Planned)

- `POST /upload` - Upload resume (PDF/DOCX/TXT)
- `POST /analyze` - Full analysis (resume + jobs)
- `POST /ats-score` - ATS compatibility score
- `POST /match-jobs` - Match resume against multiple jobs
- `POST /interview-prep/{job_id}` - Generate interview questions

## Design System

The frontend uses a cyberpunk/neon theme:
- `neon-cyan` (#00f3ff) - Primary accent
- `neon-pink` (#bc13fe) - Secondary accent
- `deep-bg` (#050505) - Dark background
- Fonts: Orbitron (display), Rajdhani (body)
