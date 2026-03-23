# ResearchRadar

> An autonomous AI-powered pipeline that monitors arXiv, summarizes papers with Gemini, scores them by relevance using semantic embeddings, and surfaces insights through a dashboard and conversational chatbot.

---

## What It Does

ResearchRadar solves a real researcher's problem: staying on top of a fast-moving field without reading dozens of papers a day.

You give it a topic (e.g. `"voice AI"` or `"diffusion models"`). It fetches the latest papers from arXiv, uses Google's Gemini to generate concise AI summaries, scores each paper for relevance using `sentence-transformers` and FAISS vector similarity, and stores everything in a PostgreSQL database. A lightweight HTML/JS frontend displays the results as a ranked dashboard with charts — and a built-in chatbot lets you ask questions about the papers directly.

The entire fetch-summarize-score-store cycle runs automatically on a schedule via APScheduler.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI Backend                   │
│                                                     │
│  Orchestrator                                       │
│  ┌──────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  arXiv   │ → │   Gemini    │ → │  Embeddings │  │
│  │  Fetcher │   │ Summarizer  │   │  + FAISS    │  │
│  └──────────┘   └─────────────┘   └──────┬──────┘  │
│                                          │          │
│                                   ┌──────▼──────┐  │
│                                   │ PostgreSQL  │  │
│                                   │  (scored)   │  │
│                                   └─────────────┘  │
│                                                     │
│  Scheduler (APScheduler) — runs pipeline on cron   │
│  /chat endpoint — Gemini 2.5 Flash conversational  │
└─────────────────────────────────────────────────────┘
              ↕ REST API
┌─────────────────────────────────────────────────────┐
│               Frontend (HTML / CSS / JS)             │
│   Ranked paper list · Relevance charts · Chatbot    │
└─────────────────────────────────────────────────────┘
```

---

## Features

- **arXiv ingestion** — fetches papers by topic using `feedparser` against the arXiv Atom feed
- **AI summarization** — each paper is summarized via Google Gemini (`gemini-2.5-flash`)
- **Semantic scoring** — papers are ranked by relevance using `sentence-transformers` embeddings and FAISS similarity search
- **Persistent storage** — papers and scores are stored in PostgreSQL via SQLAlchemy
- **Automated scheduling** — APScheduler triggers the full pipeline on a configurable interval
- **REST API** — FastAPI exposes endpoints for triggering runs, retrieving papers, and chatting
- **Dashboard** — frontend displays papers ranked by score with charts
- **AI chatbot** — `/chat` endpoint routes queries to Gemini for conversational Q&A over the results

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| Database | PostgreSQL + SQLAlchemy |
| AI summarization | Google Gemini (`google-generativeai`) |
| Embeddings | `sentence-transformers` |
| Vector search | FAISS (`faiss-cpu`) |
| Scheduling | APScheduler |
| Feed parsing | `feedparser` |
| Frontend | HTML, CSS, JavaScript |

---

## Project Structure

```
research_radar/
├── main.py                  # FastAPI app entry point, routes, lifespan
├── requirements.txt
├── app/
│   ├── agents/
│   │   └── orchestrator.py  # Coordinates fetch → summarize → score → store
│   ├── core/
│   │   ├── config.py        # Gemini client, env config
│   │   └── scheduler.py     # APScheduler setup
│   └── db/
│       ├── database.py      # SQLAlchemy session
│       └── models.py        # Paper model (title, summary, score, ...)
└── frontend/                # Dashboard UI (HTML/CSS/JS)
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally (or a connection string)
- A [Google AI Studio](https://aistudio.google.com/) API key for Gemini

### Installation

```bash
git clone https://github.com/Likhith001/research_radar.git
cd research_radar
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/research_radar
```

### Run

```bash
uvicorn main:app --reload
```

The server starts at `http://localhost:8000`. Open `frontend/index.html` in your browser for the dashboard.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/run?topic=<query>` | Trigger full pipeline for a topic |
| `GET` | `/papers` | Return all stored papers, sorted by score descending |
| `POST` | `/chat` | Send a query to the Gemini chatbot |

### Example: Run pipeline

```bash
curl "http://localhost:8000/run?topic=voice+AI"
```

### Example: Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest trends in speech recognition?"}'
```

---

## How Scoring Works

Each fetched paper's title and abstract are encoded into a dense vector using `sentence-transformers`. A query embedding (derived from the topic string) is compared against all paper vectors using FAISS cosine similarity. The resulting similarity score is stored alongside the paper, enabling ranked retrieval via the `/papers` endpoint.

---

## Roadmap

- [ ] Email digest / Slack notifications for high-scoring papers
- [ ] Topic-based filtering in the dashboard
- [ ] Support additional sources (Semantic Scholar, PubMed)
- [ ] User-defined relevance profiles
- [ ] Docker + docker-compose setup

---

## License

MIT
